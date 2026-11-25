# /// script
# requires-python = ">=3.12"
# dependencies = ["yt-dlp"]
# ///
"""Descarga los comentarios de un vídeo de YouTube y los deja en un JSON por hilos.

Uso: uv run bajar_comentarios.py <id-o-url> [--max N]

Escribe datos/comentarios-<id>.json en la carpeta desde la que se lanza y solo
imprime un resumen de tres líneas: eso es lo único que entra en el contexto.
"""

import argparse
import json
from pathlib import Path

from yt_dlp import YoutubeDL


def bajar(video: str, maximo: int) -> dict:
    """Devuelve la info del vídeo con sus comentarios, ordenados por relevancia."""
    opciones = {
        "skip_download": True,
        "getcomments": True,
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {"youtube": {"max_comments": [str(maximo), "all", "all", "20"],
                                       "comment_sort": ["top"]}},
    }
    with YoutubeDL(opciones) as ydl:
        return ydl.extract_info(video, download=False)


def por_hilos(comentarios: list[dict]) -> list[dict]:
    """Agrupa respuestas bajo su comentario raíz y marca si el canal ya contestó.

    Un hilo que abre el propio canal (p. ej. el comentario fijado) cuenta como respondido.
    """
    hilos = {c["id"]: {"id": c["id"], "autor": c["author"], "texto": c["text"],
                       "likes": c.get("like_count") or 0, "fecha": c.get("_time_text"),
                       "respuestas": 0, "respondido": bool(c.get("author_is_uploader"))}
             for c in comentarios if c["parent"] == "root"}
    for c in comentarios:
        hilo = hilos.get(c["parent"])
        if hilo:
            hilo["respuestas"] += 1
            hilo["respondido"] |= bool(c.get("author_is_uploader"))
    return sorted(hilos.values(), key=lambda h: h["likes"], reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", help="ID o URL del vídeo de YouTube")
    parser.add_argument("--max", type=int, default=2000, help="Máximo de comentarios")
    args = parser.parse_args()

    info = bajar(args.video, args.max)
    comentarios = info.get("comments") or []
    hilos = por_hilos(comentarios)
    pendientes = [h for h in hilos if not h["respondido"]]

    salida = Path("datos") / f"comentarios-{info['id']}.json"
    salida.parent.mkdir(exist_ok=True)
    salida.write_text(json.dumps({"video": info["id"], "titulo": info["title"], "hilos": hilos},
                                 ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"«{info['title']}»: {len(comentarios)} comentarios en {len(hilos)} hilos.")
    print(f"Hilos sin respuesta del canal: {len(pendientes)}.")
    print(f"Guardado en {salida}")


if __name__ == "__main__":
    main()
