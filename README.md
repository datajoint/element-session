> ## ⚠️ This is the `datajoint-2.x` branch of a fork
>
> Unofficial fork of [`datajoint/element-session`](https://github.com/datajoint/element-session),
> ported to **DataJoint 2.x**. Not affiliated with DataJoint. See
> [why this branch exists](#why-this-branch-exists) at the bottom.

[![PyPI version](https://badge.fury.io/py/element-session.svg)](http://badge.fury.io/py/element-session)

# DataJoint Element - Session

DataJoint Element for Session Management. DataJoint Elements collectively standardize
and automate data collection and analysis for neuroscience experiments.  Each Element is
a modular pipeline for data storage and processing with corresponding database tables
that can be combined with other Elements to assemble a fully functional pipeline.

Installation and usage instructions can be found at the
[Element documentation](https://docs.datajoint.com/elements/element-session/).

![element-session diagram](https://raw.githubusercontent.com/datajoint/element-session/main/images/session_diagram.svg)


---

## Why this branch exists

Upstream `element-session` was last committed on 2025-05-20 and targets DataJoint
`>=0.13`. DataJoint **2.0.0** shipped 2026-02-03 as a self-described complete
rewrite; the current release is 2.3.2. Because the element's dependency pin
admits 2.x, `pip install element-session` on a fresh environment today resolves
DataJoint 2.x and produces an installation in which the element cannot be
imported. No element had a 2.x branch and there was no open migration issue or
PR anywhere in the `datajoint` org when this fork was created.

**This branch is the complete migration, not a backward-compatible subset.**
An earlier version of this fork split the work into a `compat-fixes` branch
(changes that also work on 0.14.x) and this `datajoint-2.x` branch (adding the
2.x-only changes on top). The upstream maintainer's guidance, after reviewing
that split, was not to ship it that way: a schema is either 2.x or pre-2.x,
DataJoint no longer supports pre-2.x, and landing the backward-compatible
subset alone is actively harmful here -- it clears the import error while
leaving any `longblob`/`attach` attributes in place, which silently corrupts
data instead of loudly failing to import. See
[the migration guide](https://docs.datajoint.com/how-to/migrate-to-v20/) for
the authoritative type mapping and phase structure this follows (this is
Phase I: code only, against empty schemas, no production data touched).

Both `compat-fixes` and `datajoint-2.x` now point at the same commit and carry
the same content, kept as two names only so nothing that already referenced
either one breaks.

### Full scope of this branch

| change | count |
|---|---|
| `dj.schema` -> `dj.Schema` | 2 |
| `longblob` -> `<blob>` | 2 |
| `int` -> `int32` | 2 |
| `requirements.txt`: `datajoint>=0.13.0` -> `datajoint>=2.3` | — |

### The `longblob` change is not cosmetic

Under DataJoint 2.x a `longblob` attribute is a **raw native column**. It
declares without error and the insert succeeds, but a numpy array written to
it comes back as `bytes`:

```
longblob   (as this element declared it)   -> returned type: bytes     round-trip OK: False
<blob>     (the 2.x codec)                 -> returned type: ndarray   round-trip OK: True
```

Nothing raises. There is no warning beyond a generic "consider a core
DataJoint type" notice at declaration time that says nothing about data loss.
Traced upstream in datajoint/datajoint-python#1527: PyMySQL has no encoder for
`np.ndarray` and silently falls back to `str(value)`; the same declaration on
PostgreSQL raises instead of corrupting. See
[datajoint/element-session#43](https://github.com/datajoint/element-session/issues/43)
for the full round-trip evidence.

### Using it

```
pip install git+https://github.com/akshay-jaggi/element-session.git@datajoint-2.x
```

Pin the commit rather than the branch name if you need reproducibility. Every
change was applied mechanically (regex over each table's `definition` string,
scoped so it cannot touch a docstring or a function signature) and then
reviewed line by line; no element behaviour was altered, only attribute-type
spellings that 2.x renamed, replaced, or requires as core types.

Open PR: [datajoint/element-session#42](https://github.com/datajoint/element-session/pull/42).
