# Changelog
Notable changes to the bioturbation model are documented here.

## [Unreleased]

## [2.0.0] - 2026-05-15

### Added
- `transport_matrix` keyword argument to `run()` and `SoilProfile`, allowing the user to specify an N×N symmetric matrix of pairwise transport rates [1/s]. This enables transport between any pair of soil layers (e.g. surface↔deep), not just adjacent ones — useful for representing anecic earthworms and other preferential flow pathways.
- New example notebook `examples/non_adjacent.ipynb`.
- Input validation on `transport_matrix` (shape, symmetry, non-negativity, zero diagonal).
- Forward-Euler stability warning when `dt · max_row_sum(K) > 1`.

### Changed
- The bioturbation update is now mass-conservative. Previously, `bioturbation()` mutated layer concentrations sequentially within one time step, so the second update saw the first update's new value; algebra shows the resulting scheme only conserves mass approximately (to $O(f^2)$). The new implementation evaluates all pairwise fluxes from the old state in a single sweep, so mass is conserved exactly for any symmetric `K` in the equal-depth case. Numerical outputs of existing notebooks/calibrations shift slightly compared to v1.x.
- `SoilProfile` now stores a transport-rate matrix `self.K`; the old per-layer `bioturbation_rate` is no longer used.

### Removed
- `SoilLayer.bioturbation_rate` attribute (superseded by `SoilProfile.K`).

## [1.0.1] - 2022-03-27

### Fixed
- Corrected dependencies in `setup.cfg`.

## [1.0.0] - 2022-03-25

### Added
- First major release, including creation of Python package on PyPI.

[Unreleased]: https://github.com/samharrison7/bioturbation-model/compare/2.0.0...HEAD 
[2.0.0]: https://github.com/samharrison7/bioturbation-model/releases/tag/2.0.0
[1.0.1]: https://github.com/samharrison7/bioturbation-model/releases/tag/1.0.1
[1.0.0]: https://github.com/samharrison7/bioturbation-model/releases/tag/1.0.0
