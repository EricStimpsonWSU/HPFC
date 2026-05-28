"""Compatibility shim: re-export the std PFC simulation surface from PFC.stdPFC.

This file intentionally re-exports the implementation now located under
`PFC.stdPFC.sim_pfc_std` to preserve the historical import path.
"""

from __future__ import annotations

from PFC.stdPFC.sim_pfc_std import *

