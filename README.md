# SIGNA-ECCI (MVP)

Middleware entre ERP y LMS que concilia el estado financiero de estudiantes becados y sincroniza sus materias en el aula virtual.
Proyecto Integrador I+D+i II, Universidad ECCI. Autores: Sara Leon Fuel, Miguel David Arias Rivera.

## Historias implementadas
| HU | Endpoint |
|----|----------|
| HU-01 Consultar estado financiero | `GET /estudiantes/{id}/estado` |
| HU-02 Conciliar falsa mora | `POST /conciliacion/{id}` y `POST /webhooks/erp` |
| HU-03 Sincronizar materias con el LMS | `GET /estudiantes/{id}/materias` |
| HU-04 Mesa de ayuda digital | `POST /solicitudes`, `GET /solicitudes/{id}` |

## Ejecutar
    pip install -r requirements.txt
    pytest
    uvicorn app.main:app --reload     # docs en http://localhost:8000/docs

## Despliegue en la nube
    docker build -t signa-ecci . && docker run -p 8000:8000 signa-ecci
Compatible con Render, Railway o Cloud Run (puerto 8000).

Nota: ERP, Admisiones y LMS estan simulados en `app/data.py`; en produccion se reemplazan por conectores REST/webhooks y PostgreSQL.
