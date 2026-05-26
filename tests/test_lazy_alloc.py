import numpy as np

from HPFC.sHPFC import BackendPayloadManager
from HPFC.state import SimulationState
from HPFC.kernel_rules import KernelRules


def test_lazy_allocation(simple_model, simple_geometry, psi0, force_numpy_backend):
    mgr = BackendPayloadManager()
    kernels = KernelRules(model=simple_model, geometry=simple_geometry)

    state = SimulationState(mgr, simple_model, simple_geometry, kernels, psi0)

    # hydrodynamic buffers should not be allocated initially
    assert not getattr(state, "_v_allocated", False)
    assert state._batch_v is None

    # accessing a hydrodynamic field should allocate buffers
    _ = state.v_x
    assert state._v_allocated
    assert state._batch_v is not None
    assert state._batch_v.shape[1:] == psi0.shape

    # writing into v_x should work
    state.v_x[...] = 1.0
    assert np.all(state.v_x == 1.0)
