from __future__ import annotations

import importlib
import sys


def _alias_module(name: str, target: str, *, extra_names: tuple[str, ...] = ()):
	module = importlib.import_module(target)
	sys.modules[name] = module
	for extra_name in extra_names:
		sys.modules[extra_name] = module
	return module


backend = _alias_module(__name__ + ".backend", "backend", extra_names=("HPFC.backend",))
fft_utils = _alias_module(__name__ + ".fft_utils", "fft_utils", extra_names=("HPFC.fft_utils",))
fields = _alias_module(__name__ + ".fields", "fields", extra_names=("HPFC.fields",))
PFC2D_geometry = _alias_module(__name__ + ".PFC2D_geometry", "PFC2D_geometry", extra_names=("HPFC.PFC2D_geometry",))
PFC2D_model = _alias_module(__name__ + ".PFC2D_model", "PFC2D_model", extra_names=("HPFC.PFC2D_model",))
payload = _alias_module(__name__ + ".payload", "payload", extra_names=("HPFC.payload",))
kernel_rules = _alias_module(__name__ + ".kernel_rules", "kernel_rules", extra_names=("HPFC.kernel_rules",))
PFC2D_kernels = _alias_module(__name__ + ".PFC2D_kernels", "PFC2D_kernels", extra_names=("HPFC.PFC2D_kernels",))
state = _alias_module(__name__ + ".state", "state", extra_names=("HPFC.state",))
_simulation_facade = _alias_module(__name__ + "._simulation_facade", "_simulation_facade", extra_names=("HPFC._simulation_facade",))
steppers = _alias_module(__name__ + ".steppers", "steppers", extra_names=("HPFC.steppers",))

from .backend import (  # noqa: E402
	ARRAY_BACKEND_ENV,
	FFT_BACKEND_ENV,
	ArrayBackend,
	BackendName,
	FFTBackendName,
	_resolve_cupy_backend,
	_resolve_numpy_backend,
	_resolve_numpy_fftw_backend,
	resolve_backend,
)
from .fft_utils import batched_fftn, batched_ifftn_real, get_dc_mode, set_dc_mode  # noqa: E402
from .fields import (  # noqa: E402
	ForceBatch,
	GradBatch,
	GradMuBatch,
	PsiBatch,
	PsiGradBatch,
	VelBatch,
)
from .PFC2D_geometry import geometry_1D, geometry_2D, geometry_2D_CPU, geometry_3D  # noqa: E402
from .PFC2D_model import model_1D, model_2D, model_2D_CPU, model_3D, resolve_model_parameter  # noqa: E402
from .payload import BackendPayloadManager  # noqa: E402
from .kernel_rules import (  # noqa: E402
	KernelRules,
	_cell_volume,
	_normalize_kernel_hat_mean,
	_to_spacing_tuple,
	gaussian_kernel_fft,
)
from .PFC2D_kernels import kernels  # noqa: E402
from .state import SimulationState  # noqa: E402
from ._simulation_facade import VariantSimulationFacade  # noqa: E402
from .steppers import SHPFCTimestepper, StdPFCTimestepper  # noqa: E402

__all__ = [
	"backend",
	"fft_utils",
	"fields",
	"payload",
	"state",
	"kernel_rules",
	"PFC2D_geometry",
	"PFC2D_model",
	"PFC2D_kernels",
	"_simulation_facade",
	"steppers",
	"ArrayBackend",
	"BackendName",
	"FFTBackendName",
	"ARRAY_BACKEND_ENV",
	"FFT_BACKEND_ENV",
	"resolve_backend",
	"_resolve_numpy_backend",
	"_resolve_numpy_fftw_backend",
	"_resolve_cupy_backend",
	"get_dc_mode",
	"set_dc_mode",
	"batched_fftn",
	"batched_ifftn_real",
	"PsiBatch",
	"VelBatch",
	"GradBatch",
	"PsiGradBatch",
	"GradMuBatch",
	"ForceBatch",
	"geometry_2D",
	"geometry_2D_CPU",
	"geometry_1D",
	"geometry_3D",
	"model_2D",
	"model_2D_CPU",
	"model_1D",
	"model_3D",
	"resolve_model_parameter",
	"BackendPayloadManager",
	"KernelRules",
	"_to_spacing_tuple",
	"_cell_volume",
	"_normalize_kernel_hat_mean",
	"gaussian_kernel_fft",
	"kernels",
	"SimulationState",
	"VariantSimulationFacade",
	"StdPFCTimestepper",
	"SHPFCTimestepper",
]
