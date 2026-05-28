from __future__ import annotations

import importlib
import sys


sim_shpfc_std = importlib.import_module("HPFC.sim_shpfc_std")
sim_shpfc_div_vpsi = importlib.import_module("HPFC.sim_shpfc_div_vpsi")
sim_shpfc_psigradmu = importlib.import_module("HPFC.sim_shpfc_psigradmu")

sys.modules[__name__ + ".sim_shpfc_std"] = sim_shpfc_std
sys.modules[__name__ + ".sim_shpfc_div_vpsi"] = sim_shpfc_div_vpsi
sys.modules[__name__ + ".sim_shpfc_psigradmu"] = sim_shpfc_psigradmu

make_sim = sim_shpfc_std.make_sim

__all__ = ["sim_shpfc_std", "sim_shpfc_div_vpsi", "sim_shpfc_psigradmu", "make_sim"]
