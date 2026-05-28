import numpy as np

from HPFC.payload import BackendPayloadManager
from HPFC.state import SimulationState
from HPFC.kernel_rules import KernelRules


def test_lazy_allocation(simple_model, simple_geometry, psi0, force_numpy_backend):
    mgr = BackendPayloadManager()
    kernels = KernelRules(model=simple_model, geometry=simple_geometry)

    state = SimulationState(mgr, simple_model, simple_geometry, kernels, psi0)

    # common owned buffers and helper-backed views should be available eagerly
    assert state._batch_grad is not None
    assert state._batch_grad_mu is not None
    assert state._batch_force is not None
    assert np.shares_memory(state.psi, state._psi_poly[0])
    assert np.shares_memory(state.psi2, state._psi_poly[1])
    assert np.shares_memory(state.psi_x, state._batch_grad[0])
    assert np.shares_memory(state.grad_psi_batch.psi_y, state._batch_grad[1])
    assert np.shares_memory(state.mu_x, state._batch_grad_mu[0])
    assert np.shares_memory(state.force_y_hat, state._batch_force_hat[1])

    # hydrodynamic buffers should not be allocated initially
    assert not getattr(state, "_v_allocated", False)
    assert state._batch_v is None
    assert state._real_vel_batch is None

    # accessing a hydrodynamic field should allocate buffers
    _ = state.v_x
    assert state._v_allocated
    assert state._batch_v is not None
    assert state._real_vel_batch is not None
    assert state._batch_v.shape[1:] == psi0.shape
    assert np.shares_memory(state.v_x, state._batch_v[0])
    assert np.shares_memory(state.vel_batch.v_y, state._batch_v[1])

    # writing into v_x should work
    state.v_x[...] = 1.0
    assert np.all(state.v_x == 1.0)
