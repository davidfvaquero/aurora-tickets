# CloudWatch Agent – Aurora Tickets (Clickstream)

## Objetivo

Enviar el fichero de logs JSONL generado por la web a CloudWatch Logs.

- Fichero local: `/var/log/aurora/aurora_clickstream.jsonl`
- Log Group por alumno: `/aurora/<student_id>/clickstream`
- Log stream: `{instance_id}`

> IMPORTANTE: Cada alumno debe usar SU propio Log Group (incluye su student_id).

---

## Qué debes conseguir (Checklist)

1. ✅ El fichero `/var/log/aurora/aurora_clickstream.jsonl` existe y crece al navegar.
2. ✅ CloudWatch Agent está instalado en la EC2 de la web (EC2-6).
3. ✅ El agente está configurado para leer ese fichero.
4. ✅ Los eventos aparecen en CloudWatch → Logs → Log groups → `/aurora/<student_id>/clickstream`.

---

## Configuración (orientación)

- Usa el archivo `cw_agent_config.template.json` como base.
- Reemplaza el token `__STUDENT_ID__` por tu identificador real (el mismo que usarás en S3 y en el Dashboard).
- Guarda el config final en la ruta habitual del agente (según cómo lo instales).

Recomendación: mantén el nombre del log group EXACTO:
`/aurora/<student_id>/clickstream`

---

## Credenciales y permisos (muy importante en Academy)

En este Lab, normalmente NO se asignan IAM Roles a EC2.
CloudWatch Agent necesita credenciales válidas para enviar logs.

- El agente suele ejecutarse como `root`.
- Si tus credenciales están solo en `/home/ubuntu/.aws/credentials`, el agente puede no verlas.
- Solución típica: asegurar que el usuario que ejecuta el agente tiene acceso a credenciales válidas (por ejemplo, compartiendo credenciales al contexto de ejecución del agente).

> Prohibido: guardar claves dentro del repositorio.

---

## Validación rápida (sin comandos obligatorios)

- Comprueba que el log JSONL existe y tiene líneas JSON.
- En CloudWatch:
  - Log groups → busca tu grupo `/aurora/<student_id>/clickstream`
  - Entra al stream `{instance_id}`
  - Verifica que ves eventos con `source=client` y `source=server`.

---

## Problemas frecuentes (y cómo identificarlos)

### 1) No aparecen logs en CloudWatch

- El agente no está arrancado o no usa tu config.
- El fichero no existe o no tiene permisos de lectura.
- Credenciales/permisos insuficientes.

### 2) El log group aparece pero no hay eventos

- El agente lee un path equivocado.
- La app escribe logs en otra ruta (ver AURORA_LOG_PATH).
- El agente está leyendo “desde el final” (normal: genera nuevos eventos navegando).

### 3) Aparecen eventos pero faltan campos

- El front no está enviando ciertos campos (revisar tracker.js).
- El backend no está enriqueciendo (server-side logs).

---

## Buenas prácticas recomendadas

- Mantén un único fichero JSONL para simplificar.
- Asegura que todos los eventos incluyen: `student_id`, `timestamp`, `dt`, `session_id`, `event_type`, `source`.
- Usa siempre el mismo student_id en:
  - CloudWatch Log Group
  - Prefijo S3
  - Dashboard

Si el agente se ejecuta como root, puede requerir que las credenciales estén disponibles también para root (AWS SDK default chain). No se permite subir claves al repositorio.
