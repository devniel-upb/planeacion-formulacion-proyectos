"""
App de entregables — Planeación y Formulación de Proyectos (Maestría)

Una sola app FastAPI que expone múltiples presentaciones HTML en distintas rutas.

Cómo agregar una nueva presentación:
1. Copia el archivo .html dentro de la carpeta presentations/
   (ej. presentations/mi-otro-entregable.html)
2. (Opcional) Agrega su título y descripción en PRESENTATION_META
3. Quedará disponible automáticamente en:
   /presentaciones/mi-otro-entregable

Desarrollo local:
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python main.py            # o: uvicorn main:app --reload

Deploy en Vercel:
    Vercel detecta automáticamente la instancia `app` de FastAPI en main.py
    vc deploy
"""

import re
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI(
    title="Entregables — Planeación y Formulación de Proyectos",
    description="App única que expone las presentaciones de los entregables de la materia.",
    version="1.0.0",
)

PRESENTATIONS_DIR = Path(__file__).parent / "presentations"
MEDIA_DIR = Path(__file__).parent / "media"

# Metadatos opcionales por presentación.
# La clave es el "slug": el nombre del archivo sin la extensión .html
PRESENTATION_META = {
    "marco-logico": {
        "titulo": "Metodología de Formulación de Proyectos — Marco Lógico",
        "descripcion": (
            "Presentación interactiva: qué es, cómo se construye, la matriz 4×4, "
            "indicadores y evaluación, ventajas frente a otras metodologías y caso práctico."
        ),
    },
    "aliado-senior": {
        "titulo": "Aliado Senior 360° — Landing del Proyecto",
        "descripcion": (
            "Página principal del proyecto: el problema (árbol de problemas), los objetivos "
            "(árbol de objetivos), los servicios y el cómo (flujo, dispositivo HABLA, "
            "alcances y entregables)."
        ),
    },
    "aliado-senior-admin": {
        "titulo": "Aliado Senior 360° — Administración del Proyecto",
        "descripcion": (
            "Gestión del proyecto: riesgos y supuestos, cronograma, presupuesto, "
            "indicadores de referencia y beneficios esperados."
        ),
    },
    "aliado-senior-v1": {
        "titulo": "Aliado Senior 360° — Versión anterior (v1)",
        "descripcion": (
            "Versión anterior de la landing: problema, solución, productos, objetivos, "
            "cronograma, presupuesto, riesgos e indicadores en una sola página."
        ),
    },
    "dashboard-negocio": {
        "titulo": "Dashboard — Caso de Negocio Aliado Senior 360°",
        "descripcion": (
            "Panel ejecutivo con KPIs, gráficas de impacto, presupuesto por componente "
            "y proyecciones a 24 meses. Ideal para presentar ante la junta directiva."
        ),
    },
}


def extract_title(path: Path) -> Optional[str]:
    """Extrae el contenido de la etiqueta <title> del HTML, si existe."""
    try:
        match = re.search(
            r"<title>(.*?)</title>", path.read_text(encoding="utf-8"), re.S | re.I
        )
        return match.group(1).strip() if match else None
    except OSError:
        return None


def list_presentations() -> list:
    """Devuelve las presentaciones disponibles (archivos .html en presentations/)."""
    items = []
    for file in sorted(PRESENTATIONS_DIR.glob("*.html")):
        slug = file.stem
        meta = PRESENTATION_META.get(slug, {})
        titulo = meta.get("titulo") or extract_title(file) or slug.replace("-", " ").title()
        items.append(
            {
                "slug": slug,
                "titulo": titulo,
                "descripcion": meta.get("descripcion", ""),
            }
        )
    return items


INDEX_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Entregables — Planeación y Formulación de Proyectos</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    background: #0f172a;
    color: #e2e8f0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 70px 20px 60px;
    background-image:
      radial-gradient(ellipse at 20% 20%, rgba(56,189,248,.12), transparent 50%),
      radial-gradient(ellipse at 80% 80%, rgba(251,146,60,.08), transparent 50%);
  }}
  .tag {{
    padding: 6px 18px; border: 1px solid #38bdf8; border-radius: 999px;
    color: #38bdf8; font-size: .9rem; letter-spacing: 2px; text-transform: uppercase;
  }}
  h1 {{ font-size: clamp(1.8rem, 4vw, 2.8rem); margin-top: 22px; text-align: center; }}
  .subtitle {{ color: #94a3b8; margin-top: 10px; font-size: 1.1rem; text-align: center; }}
  .grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px; max-width: 1000px; width: 100%; margin-top: 44px;
  }}
  a.card {{
    display: block; background: #1e293b; border: 1px solid #334155; border-radius: 14px;
    padding: 26px; text-decoration: none; color: inherit;
    transition: transform .2s, border-color .2s;
  }}
  a.card:hover {{ transform: translateY(-4px); border-color: #38bdf8; }}
  a.card h2 {{ font-size: 1.2rem; color: #38bdf8; margin-bottom: 10px; }}
  a.card p {{ color: #94a3b8; font-size: .95rem; line-height: 1.5; }}
  a.card .cta {{ display: inline-block; margin-top: 16px; color: #4ade80; font-size: .92rem; font-weight: 600; }}
  .empty {{ color: #94a3b8; margin-top: 40px; }}
  code {{ background: #1e293b; padding: 2px 8px; border-radius: 6px; }}
  footer {{ margin-top: 60px; color: #475569; font-size: .85rem; }}
</style>
</head>
<body>
  <span class="tag">Maestría</span>
  <h1>Entregables</h1>
  <p class="subtitle">Planeación y Formulación de Proyectos</p>
  <div class="grid">
    {cards}
  </div>
  <footer>App construida con FastAPI · desplegada en Vercel</footer>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    """Página principal: lista todas las presentaciones disponibles."""
    presentations = list_presentations()
    if presentations:
        cards = "\n".join(
            f"""    <a class="card" href="/presentaciones/{p['slug']}">
      <h2>{p['titulo']}</h2>
      <p>{p['descripcion']}</p>
      <span class="cta">Ver presentaci&oacute;n &rarr;</span>
    </a>"""
            for p in presentations
        )
    else:
        cards = (
            "<p class='empty'>A&uacute;n no hay presentaciones. "
            "Agrega archivos .html a la carpeta <code>presentations/</code>.</p>"
        )
    return INDEX_PAGE.format(cards=cards)


@app.get("/presentaciones/{slug}", response_class=HTMLResponse)
def presentacion(slug: str):
    """Sirve la presentación HTML correspondiente al slug.

    El slug es el nombre del archivo sin extensión:
    presentations/marco-logico.html  ->  /presentaciones/marco-logico
    """
    file = PRESENTATIONS_DIR / f"{slug}.html"
    if not file.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Presentación '{slug}' no encontrada. "
            f"Revisa la lista disponible en la página principal.",
        )
    return FileResponse(file, media_type="text/html")


@app.get("/media/{filename}")
def media(filename: str):
    """Sirve recursos visuales locales usados por las presentaciones."""
    file = (MEDIA_DIR / filename).resolve()
    if MEDIA_DIR.resolve() not in file.parents or not file.is_file():
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    return FileResponse(file)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
