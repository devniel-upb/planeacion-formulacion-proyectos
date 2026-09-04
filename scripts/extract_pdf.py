"""Extrae el texto del PDF de la entrega final a un markdown legible.

Uso:
    .venv/bin/python scripts/extract_pdf.py

Salida:
    docs/entrega-final.md  (texto por página, con encabezados)
"""

from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "1. Entrega Final Planeación y Formulación de Proyectos.pdf"
OUT = ROOT / "docs" / "entrega-final.md"


def main() -> None:
    reader = PdfReader(str(PDF))
    parts = [
        "# Entrega Final — Planeación y Formulación de Proyectos",
        "",
        f"Fuente: `{PDF.name}` · {len(reader.pages)} páginas",
    ]
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        parts.append(f"\n---\n\n## Página {i}\n")
        parts.append(text.strip() or "_(sin texto extraíble)_")
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"OK -> {OUT} ({len(reader.pages)} páginas)")


if __name__ == "__main__":
    main()
