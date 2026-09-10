"""The week's weather, for the AI fit builder.

Today asks "what is it like right now" and answers it from a temperature Max
typed in. The builder asks "what is Thursday like", which nothing in the app
could answer, so this fetches a real seven-day forecast and files it in
`forecast_days`.

SOURCE. Open-Meteo — free, keyless, CC-BY 4.0, no account. The Bureau of
Meteorology was the obvious first choice and is not available: BOM's API stamps
every response with "You must not use, copy or share it". It is their internal
API, published by accident rather than on purpose. Swapping to a licensed BOM
feed later means rewriting `_fetch` and nothing else — everything below this
module speaks in `Day` objects, not in anyone's JSON.

NOTHING HERE MAY TAKE A PAGE DOWN. Same rule as the header's weather chips: a
forecast is a nicety, and an app that will not open because a weather service is
slow is worse than an app with no forecast in it. Every failure path ends in the
manual temperature Max already set.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from . import db

# Double Bay. Location is deliberately not a setting — Max lives, works and
# plays golf inside one weather cell, and a location picker would be a control
# that never gets touched. If that ever stops being true this becomes two rows
# in app_settings, not a screen.
LATITUDE = -33.8777
LONGITUDE = 151.2427
PLACE = "Sydney East · Double Bay / Rose Bay / City"
# The suburb on its own, for a line that has room for a place and not a region.
PLACE_SHORT = "Double Bay"

ENDPOINT = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code"
    # past_days as well as forecast_days: a Monday that has already been worn
    # still shows what the weather actually did, which is the whole reason the
    # week strip can be a record rather than only a plan.
    "&timezone=Australia%2FSydney&past_days=7&forecast_days=7"
)

TIMEOUT_SECONDS = 8

# WMO weather codes, written the way a person describes the sky rather than the
# way a meteorologist codes it. These strings go straight into the prompt and
# onto the day pills, so they are plain words: Claude is told "showers", never
# "code 80". Snow is in the table for completeness and will never fire here.
SKY = {
    0: "clear",
    1: "mostly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "freezing fog",
    51: "light drizzle",
    53: "drizzle",
    55: "heavy drizzle",
    56: "freezing drizzle",
    57: "freezing drizzle",
    61: "light rain",
    63: "rain",
    65: "heavy rain",
    66: "freezing rain",
    67: "freezing rain",
    71: "light snow",
    73: "snow",
    75: "heavy snow",
    77: "snow grains",
    80: "showers",
    81: "showers",
    82: "heavy showers",
    85: "snow showers",
    86: "snow showers",
    95: "thunderstorms",
    96: "thunderstorms with hail",
    99: "thunderstorms with hail",
}

# Past this, the cached week is refetched. Open-Meteo updates hourly; six hours
# keeps the forecast honest without hammering a free service every page load.
STALE_AFTER = timedelta(hours=6)


@dataclass(frozen=True)
class Day:
    """One day, in the app's vocabulary rather than the vendor's."""

    day: date
    lo: float | None
    hi: float | None
    rain_chance: int | None
    sky: str

    @property
    def key(self) -> str:
        return self.day.isoformat()

    @property
    def short(self) -> str:
        """`Today`, then `Mon`, `Tue` — the day pills in the brief."""
        return "Today" if self.day == date.today() else self.day.strftime("%a")

    @property
    def long(self) -> str:
        """`Sun 6 Sep` — the recap strip and the prompt's DAY line."""
        return f"{self.day.strftime('%a')} {self.day.day} {self.day.strftime('%b')}"

    @property
    def temp_label(self) -> str:
        if self.lo is None or self.hi is None:
            return "—"
        return f"{self.lo:g}–{self.hi:g}°C"

    @property
    def wet(self) -> bool:
        """Whether to dress for rain. 40% is the line where Max takes a coat."""
        return (self.rain_chance or 0) >= 40

    def prompt_line(self) -> str:
        rain = f", {self.rain_chance}% chance of rain" if self.rain_chance is not None else ""
        return f"{self.long} — {self.temp_label}, {self.sky}{rain}"


# ------------------------------------------------------------- fetching --


def _fetch() -> list[Day]:
    """Seven days from Open-Meteo. Raises on any failure — callers catch."""
    url = ENDPOINT.format(lat=LATITUDE, lon=LONGITUDE)
    request = urllib.request.Request(
        url, headers={"User-Agent": "wardrobe-manager (personal wardrobe app)"}
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        payload = json.loads(response.read().decode("utf-8"))

    daily = payload["daily"]
    days = []
    for index, stamp in enumerate(daily["time"]):
        code = _at(daily.get("weather_code"), index)
        days.append(
            Day(
                day=date.fromisoformat(stamp),
                lo=_at(daily.get("temperature_2m_min"), index),
                hi=_at(daily.get("temperature_2m_max"), index),
                rain_chance=_at(daily.get("precipitation_probability_max"), index),
                sky=SKY.get(code, "unsettled"),
            )
        )
    if not days:
        raise ValueError("forecast came back with no days in it")
    return days


def _at(values, index):
    """One value out of a parallel array, tolerating a short or absent one."""
    if not values or index >= len(values):
        return None
    return values[index]


# How much of the past to keep. A week back covers the Monday of the current
# week from its Friday, which is as far as any screen looks; beyond that it is
# just old weather.
KEEP_PAST = timedelta(days=14)


def refresh(conn) -> list[Day]:
    """Fetch and store the week, and the week behind it.

    Days older than KEEP_PAST go. The recent past stays: once a day is in the
    past its forecast has become a record, and the week strip reads it to say
    what Monday was actually like.
    """
    days = _fetch()
    conn.execute(
        "DELETE FROM forecast_days WHERE day < %s", (date.today() - KEEP_PAST,)
    )
    for entry in days:
        conn.execute(
            """
            INSERT INTO forecast_days
                (day, temp_min_c, temp_max_c, rain_chance_pct, sky_code, sky_label, fetched_at)
            VALUES (%s, %s, %s, %s, %s, %s, now())
            ON CONFLICT (day) DO UPDATE SET
                temp_min_c = EXCLUDED.temp_min_c,
                temp_max_c = EXCLUDED.temp_max_c,
                rain_chance_pct = EXCLUDED.rain_chance_pct,
                sky_code = EXCLUDED.sky_code,
                sky_label = EXCLUDED.sky_label,
                fetched_at = now()
            """,
            (
                entry.day,
                entry.lo,
                entry.hi,
                entry.rain_chance,
                _code_for(entry.sky),
                entry.sky,
            ),
        )
    return days


def _code_for(label: str) -> int | None:
    for code, text in SKY.items():
        if text == label:
            return code
    return None


# --------------------------------------------------------------- reading --


def _stored(conn, since: date | None = None) -> tuple[list[Day], datetime | None]:
    """Stored days from `since` on, defaulting to today.

    `since` is what lets the week strip reach backwards. The freshness check
    still reads the newest fetch across whatever was asked for, so a screen
    looking at Monday does not decide the forecast is stale because Monday's
    row was written on Monday.
    """
    rows = db.fetch_all(
        conn,
        "SELECT day, temp_min_c, temp_max_c, rain_chance_pct, sky_label, fetched_at "
        "FROM forecast_days WHERE day >= %s ORDER BY day",
        (since or date.today(),),
    )
    days = [
        Day(
            day=row["day"],
            lo=float(row["temp_min_c"]) if row["temp_min_c"] is not None else None,
            hi=float(row["temp_max_c"]) if row["temp_max_c"] is not None else None,
            rain_chance=row["rain_chance_pct"],
            sky=row["sky_label"],
        )
        for row in rows
    ]
    newest = max((row["fetched_at"] for row in rows), default=None)
    return days, newest


def week(conn, manual_temp_c: float | None = None, manual_rain: bool = False) -> list[Day]:
    """The seven days the builder offers, freshest available.

    Order of preference, and every step of it is a real situation:
      1. Stored days fetched within STALE_AFTER — the common case.
      2. A fetch, when there is nothing stored or what is stored has aged out.
      3. Stored days that are stale, when the fetch failed — yesterday's model
         run beats no weather at all.
      4. The manual temperature, repeated across seven days, when the app has
         never once reached the service. Honest rather than empty: it says the
         same thing Today says.
    """
    stored, fetched_at = _stored(conn)
    fresh = fetched_at is not None and (
        datetime.now(fetched_at.tzinfo) - fetched_at
    ) < STALE_AFTER
    if stored and fresh:
        return stored

    try:
        return refresh(conn)
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, OSError):
        # Deliberately broad and deliberately silent. The builder opens either
        # way; what it must never do is 500 because a weather service did.
        pass

    if stored:
        return stored
    return _from_manual(manual_temp_c, manual_rain)


def _from_manual(temp_c: float | None, rain: bool) -> list[Day]:
    """Seven copies of what Max typed on Today. The offline floor."""
    today = date.today()
    sky = "showers" if rain else "not known"
    return [
        Day(
            day=today + timedelta(days=offset),
            lo=temp_c,
            hi=temp_c,
            rain_chance=60 if rain else None,
            sky=sky,
        )
        for offset in range(7)
    ]


def for_week(conn, start: date, manual_temp_c: float | None = None,
             manual_rain: bool = False) -> dict[int, Day]:
    """Mon–Fri of the week beginning `start`, keyed by weekday index.

    MATCHED ON THE REAL DATE, NEVER ON THE WEEKDAY NAME. The feed returns a
    fortnight centred on today, so two Mondays are in it; a name match on a
    Thursday hands Monday's card *next* Monday's weather, confidently and
    wrongly. Days the feed does not reach are simply absent from the dict, and
    the screen draws no icon and no range for them rather than inventing one.

    Same silence as week(): a weather service must never take a screen down.
    """
    stored, fetched_at = _stored(conn, start)
    fresh = fetched_at is not None and (
        datetime.now(fetched_at.tzinfo) - fetched_at
    ) < STALE_AFTER

    if not (stored and fresh):
        try:
            refresh(conn)
            stored, _ = _stored(conn, start)
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, OSError):
            pass

    if not stored:
        stored = _from_manual(manual_temp_c, manual_rain)

    wanted = {start + timedelta(days=index): index for index in range(5)}
    return {wanted[day.day]: day for day in stored if day.day in wanted}


def find(days: list[Day], key: str | None) -> Day:
    """The selected day, defaulting to the first — never an IndexError."""
    for entry in days:
        if entry.key == key:
            return entry
    return days[0]
