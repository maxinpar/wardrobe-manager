-- 073_forecast_and_ai_fits.sql — a real week of weather, and the AI builder's answers.
--
-- Two tables for the AI build-a-fit feature, which needs to know what the week
-- looks like before it can dress Max for a day of it.
--
-- WHY A FORECAST TABLE AT ALL. The app already stores weather: one temperature
-- and one rain flag in app_settings, typed in on Today. That is a fact about
-- right now, and it is enough for "what do I wear today". The builder asks a
-- different question — "dress me for Thursday" — and there is nothing in the
-- database that knows what Thursday is like. So: seven rows, one per day,
-- refreshed from the forecast service.
--
-- The manual setting is NOT replaced. It stays what Today reads, because Max
-- looking out the window beats a model run from six hours ago, and because the
-- app must keep working with the network unplugged. This table is additive: the
-- builder prefers it, and falls back to the manual temperature when the fetch
-- has never succeeded.
--
-- SOURCE. Open-Meteo (open-meteo.com), free and keyless, CC-BY 4.0. The obvious
-- choice was the Bureau of Meteorology, and BOM's own API refuses it: every
-- response carries "You must not use, copy or share it" in its metadata. That is
-- their undocumented internal API, not a public one. If a licensed BOM feed is
-- wanted later, only wardrobe/forecast.py changes — the shape below is the
-- app's, not the vendor's.
--
-- WHY CACHE THE ANSWERS. Each build costs real money at the Anthropic API, and
-- the same brief asked twice is the same three fits. Keyed on everything that
-- can change the answer, so a re-ask with one seed added is correctly a miss.

CREATE TABLE forecast_days (
    day             date PRIMARY KEY,
    temp_min_c      numeric(4, 1),
    temp_max_c      numeric(4, 1),
    rain_chance_pct integer,
    sky_code        integer,
    sky_label       text NOT NULL,
    fetched_at      timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE forecast_days IS
  'Seven days of forecast for the Sydney East cell, refreshed from Open-Meteo. '
  'Additive to the manual weather.temp_c setting, which Today still owns: a '
  'forecast is what the builder dresses for, a look out the window is what '
  'Today dresses for.';

COMMENT ON COLUMN forecast_days.sky_code IS
  'The raw WMO weather code as delivered. Kept alongside the label so a better '
  'wording later is a re-read of this column, not a re-fetch of the week.';

COMMENT ON COLUMN forecast_days.sky_label IS
  'The plain-English sky, written for the prompt and the day pills: "clear", '
  '"showers", "overcast". This is what Claude is told; the number is not.';

-- Rows older than today are worthless — a forecast for last Tuesday is not a
-- record of last Tuesday's weather, it is a guess nobody checked. The refresh
-- deletes them rather than accumulating a fake history.

CREATE TABLE ai_fit_answers (
    brief_key       text PRIMARY KEY,
    wardrobe_mode   text NOT NULL,
    payload         jsonb NOT NULL,
    model           text NOT NULL,
    input_tokens    integer,
    output_tokens   integer,
    cached_tokens   integer,
    created_at      timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE ai_fit_answers IS
  'One row per distinct brief: the three fits Claude returned, kept so that '
  'reopening the builder does not pay for the same answer twice. The design '
  'handover listed persistence as not-done and worth doing "if the real call '
  'costs money". It does — roughly five cents an ask.';

COMMENT ON COLUMN ai_fit_answers.brief_key IS
  'sha256 over wardrobe, day, occasion, sharpness, note and the sorted seed '
  'ids. Everything that changes the answer is in the key, so a brief edited in '
  'any way misses and re-asks.';

COMMENT ON COLUMN ai_fit_answers.cached_tokens IS
  'usage.cache_read_input_tokens. Zero across repeated asks means the prompt '
  'prefix stopped being stable and the closet is being paid for every time.';

CREATE INDEX ai_fit_answers_created_idx ON ai_fit_answers (created_at DESC);
