"""Legacy compatibility shim for kernel rules.

Prefer `kernel_rules.KernelRules` for new code.
"""

from __future__ import annotations

from kernel_rules import KernelRules, _normalize_kernel_hat_mean, gaussian_kernel_fft

kernels = KernelRules

__all__ = ["KernelRules", "kernels", "_normalize_kernel_hat_mean", "gaussian_kernel_fft"]