from __future__ import annotations

import copy
import threading

from modelos import ajustar_todos

MAX_CACHE = 160
_lock = threading.Lock()
_resultados: dict = {}


def clave_estimacion(dataset_id, filtros, medida, h) -> tuple:
    recorte = tuple(sorted((filtros or {}).items()))
    return (str(dataset_id or ""), recorte, str(medida or ""), int(h))


def estimar_compartido(clave, train, h, periodo, frecuencia, progreso=None):
    """Una estimación a la vez. La misma clave reutiliza el resultado."""
    guardado = _resultados.get(clave)
    if guardado is not None:
        ajustes, train_uso, recortada = copy.deepcopy(guardado)
        return ajustes, train_uso, recortada, True

    with _lock:
        guardado = _resultados.get(clave)
        if guardado is not None:
            ajustes, train_uso, recortada = copy.deepcopy(guardado)
            return ajustes, train_uso, recortada, True
        out = ajustar_todos(train, h, periodo, frecuencia, progreso=progreso)
        _resultados[clave] = out
        while len(_resultados) > MAX_CACHE:
            _resultados.pop(next(iter(_resultados)))
        ajustes, train_uso, recortada = copy.deepcopy(out)
        return ajustes, train_uso, recortada, False
