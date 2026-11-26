<!-- BEGIN sdlc-harness (managed; do not edit this block) -->
# SDLC Harness

This project is governed by sdlc-harness. Before any workflow step, read `AGENTS.sdlc-harness.md`
for the CLI routing protocol. Role skills (`sdlc-*`) are installed in your user skill folders
(`~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`, `~/.gemini/config/skills`); load the skill named by
the `skill` field of `sdlc-harness next --run-id <id>`. If you cannot find it, STOP and tell the user
(`sdlc-harness bootstrap --project . --update-templates` reinstalls skills); never do the role without it.
Never write a challenger verdict yourself: run `sdlc-harness review --run-id <id>`. Never copy artifacts
from another run: use `sdlc-harness fork-run`. Phase artifacts, checklists and schemas live in `.harness/templates/`.
<!-- END sdlc-harness -->

## Project Notes (Harness)
- Trước khi tạo run mới (`new-run`), kiểm tra kỹ `.harness.yaml` — đặc biệt đảm bảo `requirement_sources.id_pattern` (ví dụ `REQ-[0-9]{3}` cho `docs/URD.md`) đã được khai báo khớp với định dạng mã trong tài liệu nguồn để tránh phải `fork-run` ở `BA_DRAFT`.
