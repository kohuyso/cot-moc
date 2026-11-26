# Harness Lessons Learned & Improvement Log

Tài liệu ghi nhận các vấn đề, bài học thực tế khi vận hành `sdlc-harness` để làm cơ sở review và cải tiến harness ở các phiên bản sau.

---

## Danh sách bài học

### HL-001: Thiếu `requirement_sources.id_pattern` lúc khởi tạo khiến phải `fork-run` ở `BA_DRAFT`
- **Ngày ghi nhận:** 2026-11-25
- **Run liên quan:** `cot-moc-mvp` → `cot-moc-mvp-v2`
- **Pha phát hiện:** `BA_DRAFT`
- **Trạng thái:** Open (chưa cập nhật vào `sdlc-harness`)

**Hiện tượng:**
- Khi khởi tạo run `cot-moc-mvp`, file `.harness.yaml` chỉ khai báo `requirement_sources.paths: ["docs/URD.md"]` mà chưa có `id_pattern`.
- Trong khi đó, `docs/URD.md` đã sử dụng sẵn mã định danh `REQ-001`, `REQ-002`...
- Đến bước chuẩn bị `submit_srs` ở `BA_DRAFT`, để bật source tracing theo chuẩn `REQ-[0-9]{3}`, phải cập nhật `.harness.yaml` và dùng `sdlc-harness fork-run` sang `cot-moc-mvp-v2` (do `config_snapshot` bị khóa theo từng run).

**Nguyên nhân:**
- Setup `.harness.yaml` ban đầu chưa đối chiếu định dạng mã ID trong tài liệu nguồn.
- `sdlc-harness` chưa có bước kiểm tra/cảnh báo sớm ở `INIT` hoặc `new-run` khi `requirement_sources.paths` đã cấu hình nhưng thiếu `id_pattern`.

**Đề xuất cải tiến `sdlc-harness`:**
1. Thêm preflight check / warning ở lệnh `new-run` (hoặc `start_intake`): nếu `requirement_sources.paths` được khai báo mà không có `id_pattern`, cảnh báo người dùng hoặc quét nhanh tài liệu nguồn để gợi ý pattern phổ biến (ví dụ `REQ-[0-9]{3}`).
2. Trong template `.harness.yaml` sinh ra từ `bootstrap`, bổ sung comment/ví dụ rõ ràng cho `id_pattern` đi kèm `paths`.
