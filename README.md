# planeacion-formulacion-proyectos

Monorepo para las aplicaciones relacionadas con la materia Planeación y formulación de proyectos 📈

## 📦 ¿Qué contiene?

Una app única de **FastAPI** que expone las presentaciones HTML de los distintos entregables de la materia en rutas separadas, lista para desplegarse en **Vercel**.

## 🗂️ Estructura

```
├── main.py                 # Entrypoint: instancia `app` de FastAPI
├── requirements.txt        # Dependencias (fastapi, uvicorn)
├── .gitignore
└── presentations/          # Las presentaciones HTML de los entregables
    └── marco-logico.html   # → /presentaciones/marco-logico
```

## 🛣️ Rutas

| Ruta | Descripción |
|---|---|
| `GET /` | Página principal con la lista de todos los entregables |
| `GET /presentaciones/{slug}` | Sirve la presentación `presentations/{slug}.html` |
| `GET /docs` | Documentación interactiva de la API (Swagger UI) |

## ➕ Cómo agregar un nuevo entregable

1. Copia el archivo `.html` dentro de la carpeta `presentations/`
   (ej. `presentations/mi-entregable.html`).
2. (Opcional) Agrega título y descripción en el diccionario `PRESENTATION_META`
   de `main.py`. Si no lo haces, se usa el `<title>` del propio HTML.
3. Listo: queda disponible automáticamente en `/presentaciones/mi-entregable`,
   sin tocar rutas ni reiniciar la app.

## 💻 Desarrollo local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

La app queda en `http://localhost:8000` (con recarga automática).

También puedes usar `vercel dev` si tienes la CLI de Vercel instalada.

## 🚀 Deploy en Vercel

Vercel detecta automáticamente la instancia `app` de FastAPI en `main.py`;
no se necesita configuración adicional.

**Opción A — CLI:**

```bash
vc deploy
```

**Opción B — Git:** conecta este repositorio en [vercel.com](https://vercel.com)
con *Add New Project* y despliega.
