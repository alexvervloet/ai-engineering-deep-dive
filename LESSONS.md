# Lessons learned

## Root-level unittest discovery is not universal across legacy dives

- **Expected:** the capstone README command `python -m unittest discover -v`
  would execute its tracked `tests/test_*.py` files from the submodule root.
- **Actual:** Python 3.13 reported zero tests and exited nonzero because that legacy
  `tests/` directory is not importable. Explicit `discover -s tests -v` ran 71
  tests successfully without modifying the user's dirty submodule.
- **Next time:** validate every declared root command instead of inferring it from
  prose. For legacy layouts without `tests/__init__.py`, give unittest an explicit
  start directory and retain a nonempty-suite assertion where the repo owns CI.
