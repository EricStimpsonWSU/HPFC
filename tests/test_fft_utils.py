import numpy as np

from HPFC.fft_utils import get_dc_mode, set_dc_mode, batched_fftn, batched_ifftn_real

from HPFC.payload import BackendPayloadManager


def test_get_set_dc_mode_roundtrip():
    a = np.zeros((4, 4), dtype=float)
    a[0, 0] = 2.0
    a_hat = np.fft.fftn(a)

    assert get_dc_mode(a_hat) == a_hat.flat[0]

    set_dc_mode(a_hat, 5.0)
    assert a_hat.flat[0] == 5.0


def test_batched_fft_ifft_roundtrip():
    mgr = BackendPayloadManager()
    arr = np.random.RandomState(0).randn(3, 8, 8)

    arr_hat = batched_fftn(mgr, arr)
    arr_rec = batched_ifftn_real(mgr, arr_hat)

    # real iFFT should reproduce original array within tolerance
    assert np.allclose(arr_rec, arr, atol=1e-12, rtol=1e-12)
