from __future__ import annotations


class VariantSimulationFacade:
	def __init__(self, sim, *, blocked_names: set[str] | frozenset[str] = frozenset()) -> None:
		object.__setattr__(self, "_sim", sim)
		object.__setattr__(self, "_blocked_names", frozenset(blocked_names))

	def __getattr__(self, name: str):
		if name in self._blocked_names:
			raise AttributeError(name)
		return getattr(self._sim, name)

	def __setattr__(self, name: str, value) -> None:
		if name.startswith("_"):
			object.__setattr__(self, name, value)
			return
		if name in self._blocked_names:
			raise AttributeError(name)
		setattr(self._sim, name, value)

	def __getitem__(self, key):
		return self._sim[key]

	def __setitem__(self, key, value) -> None:
		self._sim[key] = value
