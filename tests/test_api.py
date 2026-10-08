import importlib

import pytest
from fastapi.testclient import TestClient

import app.data as data
import app.main as main


@pytest.fixture()
def client():
    importlib.reload(data)
    importlib.reload(main)
    return TestClient(main.app)


def test_falsa_mora_se_concilia(client):
    assert client.get("/estudiantes/138205/estado").json()["estado_efectivo"] == "AL_DIA"
    r = client.post("/conciliacion/138205").json()
    assert r["estado_corregido"] is True
    assert r["materias_restauradas"] == ["MAT-201", "PRO-301"]


def test_materias_quedan_sincronizadas(client):
    assert client.get("/estudiantes/138205/materias").json()["desincronizadas"] == ["MAT-201", "PRO-301"]
    client.post("/webhooks/erp", json={"estudiante": "138205"})
    assert client.get("/estudiantes/138205/materias").json()["desincronizadas"] == []


def test_mora_real_no_se_corrige(client):
    r = client.post("/conciliacion/150001").json()
    assert r["estado_corregido"] is False and r["materias_restauradas"] == []


def test_mesa_de_ayuda(client):
    r = client.post("/solicitudes", json={"estudiante": "138205", "tipo": "cambio_horario"})
    assert r.status_code == 201
    assert client.get(f"/solicitudes/{r.json()['id']}").json()["estado"] == "RADICADA"


def test_estudiante_inexistente(client):
    assert client.get("/estudiantes/0/estado").status_code == 404
