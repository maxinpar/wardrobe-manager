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

ENDPOINT = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code"
    "&timezone=Australia%2FSydney&forecast_days=7"
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


def refresh(conn) -> list[Day]:
    """Fetch and store the week. Old days go — a stale guess is not history."""
    days = _fetch()
    conn.execute("DELETE FROM forecast_days WHERE day < %s", (date.today(),))
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


def _stored(conn) -> tuple[list[Day], datetime | None]:
    rows = db.fetch_all(
        conn,
        "SELECT day, temp_min_c, temp_max_c, rain_chance_pct, sky_label, fetched_at "
        "FROM forecast_days WHERE day >= %s ORDER BY day",
        (date.today(),),
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


def find(days: list[Day], key: str | None) -> Day:
    """The selected day, defaulting to the first — never an IndexError."""
    for entry in days:
        if entry.key == key:
            return entry
    return days[0]
