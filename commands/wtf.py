"""Deliver definition from urbandictionary."""

from context import get_context


def alias():
    """Define separate commands and map them to functions."""
    return {"wtf_is": get_def}


def get_def(**kwargs):
    """Lookup the string following wtf_is."""
    ctx = get_context(kwargs)
    ctx.dm_actor()
    term = ctx.text.split("wtf_is", 1)[-1].strip()
    if not term:
        return "Usage: wtf_is <term> or /wtf <term>"
    if len(term) > 30:
        return 'Search term "{0}" is too long. keep it under 30.'.format(term)
    return check_ud(term)


def check_ud(term: str) -> str:
    """Lookup against urban dictionary API."""
    import requests

    url = "https://api.urbandictionary.com/v0/define"
    try:
        response = requests.get(url, params={"term": term}, timeout=5)
    except requests.RequestException:
        return "Lookup failed for '{0}'. Try again later.".format(term)

    if not response.ok:
        return "Lookup failed for '{0}' (HTTP {1}).".format(term, response.status_code)

    data = response.json()
    entries = data.get("list") or []
    if not entries:
        return "No definition found for '{0}'.".format(term)

    definition = entries[0].get("definition", "").strip()
    example = entries[0].get("example", "").strip()
    parts = [part for part in (definition, example) if part]
    if not parts:
        return "No definition found for '{0}'.".format(term)
    return "Definition:\n{0}".format("\n\n".join(parts))
