# planeacion-formulacion-proyectos

Monorepo para las aplicaciones relacionadas con la materia Planeación y formulación de proyectos 📈

## 📦 ¿Qué contiene?

Una app única de **FastAPI** que expone las presentaciones HTML de los distintos entregables de la materia en rutas limpias, lista para desplegarse en **Vercel**.

## 🗂️ Estructura

```
├── main.py                 # Entrypoint: instancia `app` de FastAPI
├── requirements.txt        # Dependencias (fastapi, uvicorn)
├── scripts/
│   └── extract_pdf.py      # Extrae el PDF de la entrega a docs/entrega-final.md
├── docs/
│   └── entrega-final.md    # Contenido fuente extraído del PDF
├── .gitignore
└── presentations/          # Las presentaciones HTML de los entregables
    ├── marco-logico.html         # → /presentaciones/marco-logico
    ├── aliado-senior.html        # → /presentaciones/aliado-senior (landing)
    ├── aliado-senior-admin.html  # → /presentaciones/aliado-senior-admin
    ├── aliado-senior-v1.html     # → /presentaciones/aliado-senior-v1 (versión anterior)
    └── dashboard-negocio.html    # → /presentaciones/dashboard-negocio
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

## 🧭 Entregables actuales

- `/presentaciones/aliado-senior`: landing pública del caso Aliado Senior 360°. Incluye **Nosotros** (problema e imagen ampliable del árbol de problemas), **Servicios** (objetivos, componentes y servicios) y **Cómo funciona** (diagrama de flujo, dispositivo HABLA ampliable y explicación del recorrido), más un acceso a Admin.
- `/presentaciones/aliado-senior-admin`: página de administración del proyecto con matriz de riesgos coloreada, supuestos, cronograma en imagen ampliable, presupuesto, simulador interactivo de flujo de caja, indicadores y beneficios esperados.
- `/presentaciones/aliado-senior-v1`: versión anterior de la landing (historial).
- `/presentaciones/dashboard-negocio`: dashboard ejecutivo con KPIs y gráficas del caso de negocio.
- `/presentaciones/marco-logico`: presentación interactiva sobre la metodología de Marco Lógico.

## 📄 Extraer el contenido del PDF

El contenido de las presentaciones se obtiene del PDF de la entrega final. Para regenerar el markdown fuente (`docs/entrega-final.md`):

```bash
pip install pypdf
python scripts/extract_pdf.py
```

El requisito `pypdf` solo se necesita para el script de extracción (no para la app).

## 💻 Desarrollo local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

La app queda en `http://localhost:8000` (con recarga automática).

Las rutas principales de Aliado Senior no usan la extensión `.html`:

```text
http://localhost:8000/presentaciones/aliado-senior
http://localhost:8000/presentaciones/aliado-senior-admin
```

La simulación de flujo de caja permite modificar la suscripción mensual, las metas de usuarios y el costo anual. Actualiza el saldo acumulado, los ingresos, los costos y el punto de equilibrio para comparar escenarios base, optimista y de presión.

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
