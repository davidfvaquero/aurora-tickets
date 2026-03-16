// webapp/frontend/js/config.js

// ⚠️ CAMBIAR SOLO ESTO:
export const STUDENT_ID = "change_me"; // Use the same value across CloudWatch, S3, dashboard, and backend env.

// Endpoint del backend FastAPI (si el front y backend van en el mismo host, usa relativo)
export const TRACK_ENDPOINT = "/track";

// Nombre del fichero de catálogo (se genera desde events.csv -> events.json)
export const EVENTS_CATALOG_URL = "./data/events.json";

// Parámetros de sesión (cookies/localStorage)
export const SESSION_STORAGE_KEY = "aurora_session_id";
export const ATTR_STORAGE_KEY = "aurora_attribution"; // para guardar utm_campaign/referrer
export const SELECTED_EVENT_KEY = "aurora_selected_event_id";
