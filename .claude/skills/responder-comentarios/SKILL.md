---
name: responder-comentarios
description: Prepara borradores de respuesta a los comentarios de un vídeo de YouTube del canal. Úsala cuando pida contestar, revisar o ponerse al día con los comentarios de un vídeo, o cuando pegue un ID o una URL de YouTube hablando de comentarios.
argument-hint: "[id-o-url-del-video]"
disable-model-invocation: true
allowed-tools: Bash(uv run ${CLAUDE_SKILL_DIR}/scripts/bajar_comentarios.py *)
---

# Responder comentarios de YouTube

Tú redactas, yo publico. Nunca publiques ni contestes nada en YouTube: solo dejas borradores en un fichero.

## Pasos

1. **Descarga.** Ejecuta `uv run ${CLAUDE_SKILL_DIR}/scripts/bajar_comentarios.py $ARGUMENTS`.
   Deja el JSON en `datos/` e imprime un resumen. No abras el JSON tú.
2. **Clasifica con el subagente.** Pásale al subagente `clasificador-comentarios` la ruta del JSON que ha
   impreso el script. Él lo lee entero en su propio contexto y te devuelve una tabla corta. Tú trabajas solo
   con esa tabla.
3. **Cursos.** Para cada hilo de la categoría «pide curso», busca el curso con la herramienta `buscar_curso`
   del servidor MCP `catalogo`. Usa la URL que devuelva, tal cual. Si no hay ninguno que encaje, dilo en el
   borrador; no inventes una URL.
4. **Borradores.** Escribe `respuestas/<id-del-video>.md` con un bloque por hilo: autor, una línea con lo que
   dice y tu borrador de respuesta.

## Cómo respondo

- De tú a tú, frases cortas. Dos o tres líneas como mucho.
- En el idioma del comentario.
- Si es una pregunta técnica, la respuesta concreta. Si no la sabes seguro, dilo y no la inventes.
- Si piden algo que prometí en el vídeo (repo, plantilla, tutorial), enlázalo solo si ya existe. Si no, «está
  en camino» y nada más.
- A un hater, una línea educada o nada. Nunca discutas.
- Nada de «¡Gracias por tu comentario!» de plantilla, nada de emojis en cadena.
- Si muchos piden lo mismo, no repitas la misma frase: YouTube marca como spam las respuestas idénticas con
  enlace. Varía el texto y menciona algo de cada comentario.
- Spam y estafas: no se responden, se listan al final para que yo los borre.
