"""Legacy compatibility shim for kernel rules.

Prefer `kernel_rules.KernelRules` for new code.
"""

from __future__ import annotations

from PFC.Core.kernel_rules import KernelRules, _cell_volume, _normalize_kernel_hat_mean, _to_spacing_tuple, gaussian_kernel_fft

kernels = KernelRules

__all__ = ["KernelRules", "kernels", "_to_spacing_tuple", "_cell_volume", "_normalize_kernel_hat_mean", "gaussian_kernel_fft"]
