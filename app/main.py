from itertools import count

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import data
from .conciliacion import conciliar, estado_efectivo

app = FastAPI(title="SIGNA-ECCI", version="0.1.0")
_ids = count(1)


class Solicitud(BaseModel):
    estudiante: str
    tipo: str  # cambio_horario | ajuste_materia | cierre_ciclo
    detalle: str = ""


def _req(est_id: str):
    if est_id not in data.ERP:
        raise HTTPException(404, "Estudiante no encontrado")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/estudiantes/{est_id}/estado")  # HU-01
def estado(est_id: str):
    _req(est_id)
    f = data.ERP[est_id]
    return {"estudiante": est_id, "beca": f["beca"], "estado_erp": f["estado_financiero"],
            "estado_efectivo": estado_efectivo(est_id)}


@app.get("/estudiantes/{est_id}/materias")  # HU-03
def materias(est_id: str):
    _req(est_id)
    adm, lms = set(data.ADMISIONES[est_id]), data.LMS[est_id]
    return {"inscritas": sorted(adm), "en_aula_virtual": sorted(lms), "desincronizadas": sorted(adm - lms)}


@app.post("/conciliacion/{est_id}")  # HU-02
def ejecutar(est_id: str):
    _req(est_id)
    return conciliar(est_id)


@app.post("/webhooks/erp")  # evento de cierre de ciclo desde el ERP
def webhook(evento: dict):
    est = str(evento.get("estudiante", ""))
    _req(est)
    return conciliar(est)


@app.post("/solicitudes", status_code=201)  # HU-04 mesa de ayuda
def crear(s: Solicitud):
    _req(s.estudiante)
    sid = next(_ids)
    data.SOLICITUDES[sid] = {"id": sid, **s.model_dump(), "estado": "RADICADA"}
    return data.SOLICITUDES[sid]


@app.get("/solicitudes/{sid}")
def ver(sid: int):
    if sid not in data.SOLICITUDES:
        raise HTTPException(404, "Solicitud no encontrada")
    return data.SOLICITUDES[sid]
