from __future__ import annotations

import importlib
import sys


sim_pfc_std = importlib.import_module("HPFC.sim_pfc_std")
sys.modules[__name__ + ".sim_pfc_std"] = sim_pfc_std

build_model = sim_pfc_std.build_model
make_sim = sim_pfc_std.make_sim

__all__ = ["sim_pfc_std", "build_model", "make_sim"]
