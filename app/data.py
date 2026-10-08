"""Datos simulados de ERP (finanzas), Admisiones y LMS (Moodle/Canvas).
En produccion se reemplazan por conectores REST/webhooks reales."""

ERP = {
    "138205": {"nombre": "Camila Torres", "beca": True, "estado_financiero": "MORA_FALSA", "ciclo_cerrado": False},
    "141063": {"nombre": "Andres Rojas", "beca": True, "estado_financiero": "AL_DIA", "ciclo_cerrado": True},
    "150001": {"nombre": "Laura Mendez", "beca": False, "estado_financiero": "MORA", "ciclo_cerrado": True},
}
ADMISIONES = {
    "138205": ["ING-101", "MAT-201", "PRO-301"],
    "141063": ["ING-101", "PRO-301"],
    "150001": ["MAT-201"],
}
LMS = {
    "138205": {"ING-101"},  # faltan MAT-201 y PRO-301: desincronizacion
    "141063": {"ING-101", "PRO-301"},
    "150001": {"MAT-201"},
}
SOLICITUDES: dict[int, dict] = {}
