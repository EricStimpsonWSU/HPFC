"""Compatibility shim package for legacy HPFC import paths.

These modules re-export the corresponding implementations from the modern
`PFC` package so tests and external code importing `HPFC.*` continue to work.
"""

__all__ = [
    "sim_pfc_std",
    "sim_shpfc_std",
    "sim_shpfc_div_vpsi",
    "sim_shpfc_psigradmu",
]
