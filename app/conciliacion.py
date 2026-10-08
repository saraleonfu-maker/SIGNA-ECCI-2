from . import data


def estado_efectivo(est_id: str) -> str:
    """Concilia el estado financiero: un becado con ciclo sin cerrar NO esta en mora real."""
    f = data.ERP[est_id]
    if f["beca"] and not f["ciclo_cerrado"] and f["estado_financiero"] == "MORA_FALSA":
        return "AL_DIA"
    return "AL_DIA" if f["estado_financiero"] == "AL_DIA" else "MORA"


def conciliar(est_id: str) -> dict:
    """Corrige el falso estado de mora y sincroniza materias faltantes en el LMS."""
    if est_id not in data.ERP:
        raise KeyError(est_id)
    corregido = False
    f = data.ERP[est_id]
    if estado_efectivo(est_id) == "AL_DIA" and f["estado_financiero"] != "AL_DIA":
        f["estado_financiero"], f["ciclo_cerrado"] = "AL_DIA", True
        corregido = True
    restauradas = []
    if f["estado_financiero"] == "AL_DIA":
        faltantes = set(data.ADMISIONES[est_id]) - data.LMS[est_id]
        data.LMS[est_id] |= faltantes
        restauradas = sorted(faltantes)
    return {"estudiante": est_id, "estado_corregido": corregido, "materias_restauradas": restauradas}
