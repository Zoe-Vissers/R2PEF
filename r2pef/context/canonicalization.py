"""Canonicalization helpers.

Two functions live here:

- ``local_name(s)`` is used everywhere the framework needs to compare a CPGM
  string against a source IRI when the CPGM only retains the bare local name
  or a synthetic prefixed form.

- ``object_variants(o)`` returns every plausible string form of a single
  triple object, used to make PGIU↔source triple comparison robust against
  the "is this string quoted as a literal or bare as an IRI" ambiguity.

local_name rule
---------------
- Literals (start+end with ``"``) and rdflib datatype-tagged literals are
  passed through unchanged.
- Else: try ``#``, then ``/``, then ``:`` (last separator wins).
- Else: if the string matches a synthetic prefix pattern like ``nss9_Foo``
  or ``ns1_bar`` (a short alphanumeric token + underscore + the rest),
  return the suffix. This is asymmetric on purpose — source IRIs from
  rdflib never carry that shape, so is is only needed to match the CPGM
  side back to the source.
- Else: return the string unchanged.
"""
from __future__ import annotations

import re

# Synthetic prefix used by some adapters in `namespace_plus_local` forms.
# Matches:
#     nss1_eligibleQuantity        → eligibleQuantity
#     ns42_parentCountry           → parentCountry
#     ogp_tag                      → tag
#     a_b                          → b
# but NOT:
#     blank_node_id                → unchanged (would over-eat)
# To stay conservative only short alphanumeric prefixes are accepted (≤ 8
# chars, alpha + digits, starting with a letter).
_SYNTHETIC_PREFIX = re.compile(r"^[A-Za-z][A-Za-z0-9]{0,7}_(?P<rest>[A-Za-z][A-Za-z0-9_]*)$")


def local_name(s: str) -> str:
    """Best-effort local-name extraction.

    >>> local_name("http://example.org/Movie")
    'Movie'
    >>> local_name("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    'type'
    >>> local_name("ex:Movie")
    'Movie'
    >>> local_name("nss9_parentCountry")
    'parentCountry'
    >>> local_name("nss1_eligibleQuantity")
    'eligibleQuantity'
    >>> local_name("Movie")
    'Movie'
    >>> local_name('"Django Unchained"')
    '"Django Unchained"'
    >>> local_name("http://example.org/Offer686/")
    'Offer686'
    """
    if not s:
        return s
    # Literals pass through verbatim.
    if s.startswith('"') and (s.endswith('"') or '"^^' in s):
        return s

    if "#" in s:
        # Strip a trailing '#' (rare but possible) so we don't return "".
        tail = s.rsplit("#", 1)[-1]
        if tail:
            return tail
        # If the URI ends with '#', fall back to whatever lies before it.
        return local_name(s[:-1])
    if "/" in s:
        tail = s.rsplit("/", 1)[-1]
        if tail:
            return tail
        # Trailing-slash IRIs like ``http://example.org/Offer686/`` would
        # otherwise reduce to ``""`` and collapse every such IRI into a
        # single ln_index bucket. Strip one trailing '/' and recurse.
        return local_name(s[:-1])
    # Prefixed form via colon — only the *last* colon counts.
    if ":" in s and not s.startswith("_:"):
        tail = s.rsplit(":", 1)[-1]
        if tail:
            return tail
        return local_name(s[:-1])

    # Synthetic underscore-prefix form used by adapters in
    # ``namespace_plus_local`` encodings. Conservative — see _SYNTHETIC_PREFIX.
    m = _SYNTHETIC_PREFIX.match(s)
    if m:
        return m.group("rest")

    return s


def unquote_literal(s: str) -> str:
    """If ``s`` is a quoted literal (``"…"``), return the lexical value.

    Used at comparison sites that need to compare quoted ↔ unquoted
    versions of the same object.
    """
    if isinstance(s, str) and len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


def quote_literal(s: str) -> str:
    """Inverse of :func:`unquote_literal` — wrap if not already wrapped."""
    if isinstance(s, str) and len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        return s
    return f'"{s}"'


def object_variants(o: str) -> set:
    """Every comparable form of a triple object.

    A CPGM literal-form value may legitimately carry either an IRI or a
    real literal string. To compare robustly both the quoted and unquoted 
    variant of every object position is indexed and looked up. Subjects 
    and predicates are unambiguous (always IRIs in source RDF) and are not 
    expanded.

    >>> sorted(object_variants("http://example.org/X"))
    ['"http://example.org/X"', 'http://example.org/X']
    >>> sorted(object_variants('"Django Unchained"'))
    ['"Django Unchained"', 'Django Unchained']
    """
    if not isinstance(o, str):
        return {o}
    return {o, unquote_literal(o), quote_literal(o)}