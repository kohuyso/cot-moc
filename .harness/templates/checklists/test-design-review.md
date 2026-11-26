# Checklist: Thẩm định Thiết kế Kiểm thử (ISO/IEC/IEEE 29119-3 Test Design Review)

Bộ checklist bắt buộc dành cho **Lead QA / Test Architect Challenger** trong pha `TEST_DESIGN_REVIEW` để thẩm định chất lượng bộ test case trước khi bàn giao cho Dev lập trình.

---

## 1. Tính hoàn chỉnh của Tài liệu (Completeness)
- [ ] Tồn tại `artifacts/test-plan.md` đạt chuẩn ISO 29119-3 (mô tả chiến lược, scope, out-of-scope, môi trường test).
- [ ] Tồn tại `artifacts/test-cases.json` hợp lệ 100% theo schema `test-cases.schema.json`.
- [ ] Tất cả test case đều có đầy đủ: `id` (chuẩn `TC-xxx`), `requirement_id` (`FR-xxx`), `title`, `tier`, `type`, `priority`, `steps`, `expected_result`.

---

## 2. Ma trận bao phủ yêu cầu (100% RTM Coverage)
- [ ] Mọi `FR-xxx` trong `requirement.json` và `rtm.md` đều có ít nhất 1 test case tương ứng.
- [ ] Các tiêu chí chấp nhận (Acceptance Criteria - Given/When/Then) trong FSD đều được mô tả thành các bước test cụ thể.
- [ ] Không có test case ảo hoặc dùng lệnh build hệ thống (`npm run build`, `dotnet build`) làm test ID.

---

## 3. Độ sâu kiểm thử tiêu cực & Giá trị biên (Negative & Boundary Depth)
- [ ] **Negative Cases**: Toàn bộ mã lỗi `ERR-xxx` trong FSD đều có test case kích hoạt.
- [ ] **Boundary Cases**: Các trường số tiền, số lượng, ngày tháng từ Từ điển dữ liệu (`data-dictionary.md`) có test case kiểm tra biên:
  - Giá trị nhỏ nhất (0 hoặc số âm)
  - Giá trị lớn nhất (vượt hạn mức/ngân sách)
  - Giá trị NULL / rỗng / ký tự đặc biệt
- [ ] **Security Cases**: Kiểm thử phân quyền (Role Unauthorized), token hết hạn, input injection.
- [ ] **Số liệu đo (ghi số, không ghi "đạt")**: tổng case = __; `NEGATIVE`+`BOUNDARY`+`SECURITY` = __ (__%, sàn `quality_floor.test_negative_boundary_min_ratio`, mặc định khuyến nghị 30%); `E2E_UI` = __ (__%); FR không có case = __; `automated_test_ref` không trỏ file thật = __; chữ ký bước phổ biến nhất sau khi xoá mã FR/số = __/__ case.
- [ ] Mọi FR có `exception_flows` đều có ít nhất 1 case `NEGATIVE`/`BOUNDARY`.

---

## 4. Phân tầng kiểm thử (Test Tiering & Feasibility)
- [ ] Đối với tính năng có giao diện, có ít nhất 1 test case tầng `E2E_UI`.
- [ ] Đối với tính năng nâng cấp/bảo trì (`maintain_upgrade`), có test case tầng `REGRESSION`.
- [ ] Tiêu chí kết quả mong đợi (`expected_result`) rõ ràng, có thể tự động hóa (không mô tả cảm tính kiểu "hệ thống chạy tốt").

---

## 5. Tiêu chuẩn Kết luận (Verdict Protocol)
- **APPROVE**: 100% RTM coverage đạt, có đủ Positive/Negative/Boundary, không có finding mức BLOCKER/HIGH.
- **PUSHBACK**: Phát hiện sót requirement trong RTM, thiếu test case tiêu cực hoặc test case sơ sài $\rightarrow$ Trả về `TEST_DESIGN` kèm danh sách remediation rõ ràng.
