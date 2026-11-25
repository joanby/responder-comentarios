# Demo: responder los comentarios de un vídeo con una skill, un subagente y un MCP

Proyecto del vídeo *Skills, MCP o subagentes*. Cada pieza hace lo que le toca:

| Pieza | Fichero | Qué aporta |
|---|---|---|
| Skill `responder-comentarios` | `.claude/skills/responder-comentarios/SKILL.md` | El oficio: los pasos y cómo respondo yo |
| Script de la skill | `.claude/skills/responder-comentarios/scripts/bajar_comentarios.py` | Baja los comentarios con `yt-dlp`. Claude solo ve su resumen |
| Subagente `clasificador-comentarios` | `.claude/agents/clasificador-comentarios.md` | Lee cientos de comentarios en su propio contexto y devuelve una tabla |
| Servidor MCP `catalogo` | uno propio con una herramienta `buscar_curso` (no incluido en este repo) | Las URL de los cursos, vivas y desde un servidor compartido |

## Probarlo

```bash
claude mcp add --transport http catalogo https://TU_DOMINIO/mcp \
  --header "Authorization: Bearer TU_TOKEN"
claude
> /responder-comentarios https://youtu.be/ID_DEL_VIDEO
```

Sin un servidor MCP `catalogo`, la skill funciona igual salvo el paso 3: no podrá buscar las URL de los cursos.

Requiere [Claude Code](https://code.claude.com) y [uv](https://docs.astral.sh/uv/).

El resultado queda en `respuestas/<id>.md`. Los comentarios se publican a mano en YouTube Studio: la skill
nunca contesta por ti.

`datos/` y `respuestas/` se generan al ejecutar y no se versionan.
