### Summary

Make each `sim_[model]_[variant].py` module **declare the model parameters it actually requires** and provide the kernel-builder it uses. Remove the global fallback that *assumes* `rho0` and `Gamma_s`. Concretely:

- Add a small, explicit API in each sim module (e.g., `REQUIRED_MODEL_PARAMS`, optional `OPTIONAL_MODEL_PARAMS`, and `build_lin_kernels`).
- Make `build_model` accept only those parameters (or accept `**kwargs` and validate against the declared lists).
- Change `KernelRules` to call the sim module's `build_lin_kernels` (as it already tries) and **fail** if the sim module does not provide one, instead of using a generic fallback that requires `rho0`/`Gamma_s`.

Below I give a minimal design, example code changes, and a migration plan.

---

### Why (evidence from your code)

The current `stdPFC` sim defines `build_model` with `rho0` and `Gamma_s` even though the standard PFC variant doesn't use them:

> `def build_model(*, temp: float, beta: float, Gamma: float, rho0: float, Gamma_s: float, dt: float) -> model_2D:`  
> `    rho0 = resolve_model_parameter(model, "rho0")` . 

Because the core `KernelRules` contains a generic fallback that *assumes* those parameters, every model is forced to provide them even when unused. The fix is to make each sim module explicitly state what it needs.

---

### Minimal API proposal

Add the following small, conventional items to every `sim_*.py`:

```py
# in sim_foo_bar.py
REQUIRED_MODEL_PARAMS = ("temp", "beta", "Gamma", "dt")
OPTIONAL_MODEL_PARAMS = {"rho0": 1.0, "Gamma_s": None}  # optional defaults (if any)

def build_model(*, temp: float, beta: float, Gamma: float, dt: float, **kwargs):
    # validate kwargs against OPTIONAL_MODEL_PARAMS if present
    return FooModel(temp=temp, beta=beta, Gamma=Gamma, dt=dt, **kwargs)

def build_lin_kernels(model, geometry):
    # compute only the kernels this sim needs
    ...
```

**Rules**
- `REQUIRED_MODEL_PARAMS` is a tuple of names the sim *must* receive.
- `OPTIONAL_MODEL_PARAMS` is a dict of optional names and defaults (or `None` to indicate optional but no default).
- `build_model` should accept exactly the required params (plus `**kwargs` for optional ones) and construct a model object tailored to that sim (preferably a small dataclass).

---

### Changes to Core (`KernelRules` and `PFC2D_model`)

1. **Remove or narrow the generic fallback** in `KernelRules.__post_init__`. Instead of building a generic `_build_from_generic_model` that assumes `rho0`/`Gamma_s`, require the sim module to provide `build_lin_kernels`. If not present, raise a clear `AttributeError` telling the sim to declare its required params and kernel builder.

2. **Add a small helper** in `PFC.Core` to validate model parameters before constructing the model:

```py
# Core/utils.py (new)
def validate_model_params(sim_module, provided_params: dict):
    required = getattr(sim_module, "REQUIRED_MODEL_PARAMS", ())
    missing = [p for p in required if p not in provided_params]
    if missing:
        raise TypeError(f"Missing required model params for {sim_module.__name__}: {missing}")
```

3. **Use per-sim model dataclasses** rather than the monolithic `model_2D` that always requires `rho0` and `Gamma_s`. Keep `model_2D` as a generic fallback for legacy sims, but prefer sim-specific dataclasses.

---

### Concrete code snippets

**A. `stdPFC` (before → after)**

*Before (excerpt you have):*
```py
def build_model(*, temp: float, beta: float, Gamma: float, rho0: float, Gamma_s: float, dt: float) -> model_2D:
    base = model_2D(temp=temp, beta=beta, Gamma=Gamma, rho0=rho0, Gamma_s=Gamma_s, dt=dt)
    return base
```

*After (only the params stdPFC actually needs):*
```py
REQUIRED_MODEL_PARAMS = ("temp", "beta", "Gamma", "dt")
OPTIONAL_MODEL_PARAMS = {}  # none for stdPFC

@dataclass
class StdPFCModel:
    temp: float
    beta: float
    Gamma: float
    dt: float

def build_model(*, temp: float, beta: float, Gamma: float, dt: float) -> StdPFCModel:
    return StdPFCModel(temp=float(temp), beta=float(beta), Gamma=float(Gamma), dt=float(dt))
```

**B. `KernelRules` change (high level)**

Replace the current fallback block with:

```py
# inside KernelRules.__post_init__
sim_build = None
try:
    sim_mod_name = getattr(self.model.__class__, "__module__", None)
    if sim_mod_name:
        sim_mod = importlib.import_module(sim_mod_name)
        sim_build = getattr(sim_mod, "build_lin_kernels", None)
except Exception:
    sim_build = None

if sim_build is None:
    raise AttributeError(
        f"Simulation module {sim_mod_name!r} must provide build_lin_kernels(model, geometry) "
        "and declare REQUIRED_MODEL_PARAMS; no generic fallback is used."
    )
# then call sim_build(self.model, self.geometry)
```

This forces each sim to provide the kernel builder that knows which model attributes it needs.

---

### Migration steps

1. **Add `REQUIRED_MODEL_PARAMS` and `build_model` changes** to each `sim_*.py`. For `stdPFC` remove `rho0`/`Gamma_s` from the signature if unused.
2. **Add `build_lin_kernels`** to any sim that currently relies on the generic fallback (most of your sHPFC variants already have `build_lin_kernels` — keep them).
3. **Update any code that constructs models** (tests, examples, CLI) to pass only the declared parameters or to call a small validator helper that maps user-provided config into the sim's `build_model`.
4. **Run tests**: KernelRules will now raise a clear error if a sim module lacks `build_lin_kernels` — fix those sims by adding the function or by explicitly opting into the legacy `model_2D` shape.
5. **Optional**: provide a small compatibility shim for older configs that still supply `rho0`/`Gamma_s` by mapping them into optional kwargs for sims that accept them.

---

### Benefits

- **No more unused required params**: sims declare exactly what they use.
- **Clearer errors**: missing kernel builder or missing params are explicit.
- **Extensible**: new models can declare their own required/optional params and kernel builders without touching core code.
- **Safer refactor**: you can later convert sim-specific model dataclasses into typed configs or pydantic models.
