"""The Cloudflare Access gate, and specifically the ways it must say no.

This is the one piece of the app where being wrong is not a display bug: the
tunnel puts wardrobe.maxboucoiran.com on the public internet, and behind it sits
an API key that costs real money per request. The tests that matter here are the
refusals, so most of this file is forged, stale, borrowed and mis-addressed
tokens, each of which must bounce.

The signing key is generated here and Cloudflare's JWKS lookup is replaced with
it, so the whole thing runs offline and without a Cloudflare account.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from wardrobe import access  # noqa: E402

TEAM = "maxteam.cloudflareaccess.com"
AUD = "a1b2c3d4e5f6000000000000000000000000000000000000000000000000abcd"
MAX = "maxime.boucoiran@gmail.com"

KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
OTHER_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture(autouse=True)
def configured(monkeypatch):
    """Access switched on, and its key lookup pointed at ours."""
    monkeypatch.setenv("CF_ACCESS_TEAM_DOMAIN", TEAM)
    monkeypatch.setenv("CF_ACCESS_AUD", AUD)
    monkeypatch.setenv("CF_ACCESS_ALLOWED_EMAILS", MAX)

    class FakeKey:
        key = KEY.public_key()

    class FakeClient:
        def get_signing_key_from_jwt(self, token):
            return FakeKey()

    monkeypatch.setattr(access, "_client", lambda: FakeClient())


def token(key=KEY, **overrides) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    claims = {
        "aud": AUD,
        "iss": f"https://{TEAM}",
        "email": MAX,
        "iat": now,
        "exp": now + dt.timedelta(hours=1),
    }
    claims.update(overrides)
    return jwt.encode(claims, key, algorithm="RS256")


# ------------------------------------------------------------ the yes --


def test_a_properly_signed_token_for_max_gets_in():
    assert access.identity(token()) == MAX


def test_the_email_is_matched_case_insensitively():
    assert access.identity(token(email="Maxime.Boucoiran@Gmail.com")) == MAX


# ------------------------------------------------------------- the no --


def test_no_token_at_all_is_refused():
    with pytest.raises(access.Denied):
        access.identity("")


def test_a_token_signed_with_the_wrong_key_is_refused():
    """The whole point. The header is forgeable; the signature is not."""
    with pytest.raises(access.Denied):
        access.identity(token(key=OTHER_KEY))


def test_an_unsigned_token_is_refused():
    """`alg: none`, the oldest trick there is."""
    forged = jwt.encode(
        {"aud": AUD, "iss": f"https://{TEAM}", "email": MAX}, None, algorithm="none"
    )
    with pytest.raises(access.Denied):
        access.identity(forged)


def test_an_expired_token_is_refused():
    past = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=2)
    with pytest.raises(access.Denied):
        access.identity(token(exp=past, iat=past - dt.timedelta(hours=1)))


def test_a_token_for_another_access_application_is_refused():
    """Valid, Cloudflare-signed, and minted for a different app of Max's."""
    with pytest.raises(access.Denied):
        access.identity(token(aud="f" * 64))


def test_a_token_from_another_cloudflare_team_is_refused():
    with pytest.raises(access.Denied):
        access.identity(token(iss="https://someoneelse.cloudflareaccess.com"))


def test_somebody_elses_google_account_is_refused():
    """Access lets them through the edge; the allow-list is the second lock."""
    with pytest.raises(access.Denied):
        access.identity(token(email="someone.else@gmail.com"))


def test_a_token_with_no_email_is_refused():
    with pytest.raises(access.Denied):
        access.identity(token(email=""))


def test_an_empty_allow_list_admits_nobody(monkeypatch):
    """Misconfiguration must fail closed, including for Max himself."""
    monkeypatch.setenv("CF_ACCESS_ALLOWED_EMAILS", "")
    with pytest.raises(access.Denied):
        access.identity(token())


def test_a_jwks_lookup_failure_denies_rather_than_admits(monkeypatch):
    """The network being down and someone trying it on look the same. Both no."""

    class Broken:
        def get_signing_key_from_jwt(self, token):
            raise RuntimeError("cloudflare unreachable")

    monkeypatch.setattr(access, "_client", lambda: Broken())
    with pytest.raises(access.Denied):
        access.identity(token())


# ----------------------------------------------------- switched off --


def test_unset_aud_means_not_configured(monkeypatch):
    """Local development: no Access, no gate, unchanged."""
    monkeypatch.delenv("CF_ACCESS_AUD", raising=False)
    assert access.configured() is False


def test_team_without_aud_is_not_configured(monkeypatch):
    """Half-configured is off, not on-and-broken — one alone cannot verify."""
    monkeypatch.delenv("CF_ACCESS_AUD", raising=False)
    monkeypatch.setenv("CF_ACCESS_TEAM_DOMAIN", TEAM)
    assert access.configured() is False
