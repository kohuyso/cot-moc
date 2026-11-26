# Change Brief: [Tiêu đề thay đổi]

> Luồng: hotfix | minor. Phiếu thay đổi ngắn, thay cho SRS đầy đủ. Mỗi heading `##` dưới đây là bắt buộc.
> Đi kèm `artifacts/requirement.json` (cùng schema và cùng kiểm tra với SRS) và `artifacts/implementation-plan.md` ngắn.

## Vấn đề

[Mô tả triệu chứng hoặc nhu cầu: ai bị ảnh hưởng, xảy ra khi nào, mức độ nghiêm trọng. Trích dẫn yêu cầu gốc của người dùng.]

## Nguyên nhân gốc

[Hotfix: bắt buộc, nêu nguyên nhân gốc đã xác minh, kèm bằng chứng (log, bước tái hiện, dòng code).
Minor: nêu lý do cần thay đổi hoặc điểm mở rộng.]

## Phạm vi

- [File / module / hành vi sẽ thay đổi]
- Số file dự kiến: [n] (không vượt `track_limits.max_files`)
- Số dòng dự kiến: [n] (không vượt `track_limits.max_lines`)

## Ngoài phạm vi

- [Hành vi, file, thay đổi liên quan cố ý KHÔNG làm trong phiếu này]

## Tiêu chí chấp nhận

- **AC-001**: Given [bối cảnh], When [hành động], Then [kết quả quan sát được].
- **AC-002**: Given [bối cảnh], When [hành động], Then [kết quả quan sát được].

## Rủi ro

| Rủi ro | Khả năng | Ảnh hưởng | Giảm thiểu |
|---|---|---|---|
| [Rủi ro hồi quy / phụ thuộc] | Thấp/Vừa/Cao | Thấp/Vừa/Cao | [Biện pháp] |

## Rollback

[Cách hoàn tác an toàn nếu thay đổi gây lỗi: revert commit, tắt feature flag, khôi phục dữ liệu. Nêu ai thực hiện và mất bao lâu.]

## Kế hoạch sửa

1. [Bước 1: viết test REGRESSION/failing test trước; hotfix: ghi vào `test-cases.json` với `type: REGRESSION`]
2. [Bước 2: thay đổi tối thiểu trong file đã nêu ở Phạm vi]
3. [Bước 3: chạy lint, typecheck, test; thu bằng chứng]
