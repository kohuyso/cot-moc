# UI/UX Specification: [Feature / System Name]

## 1. Executive Summary & Change Scope
- **Run ID**: `[run-id]`
- **Feature Name**: `[Feature Name / Bugfix]`
- **Change Type**: `[Maintain / Upgrade / New Feature]`
- **Target Route / Screens**: `[/booth, /draw, etc.]`
- **Target Frontend Files / Components**:
  - `[frontend/src/pages/TargetPage.tsx]`
  - `[frontend/src/components/TargetComponent.tsx]`

---

## 2. Real Page Baseline & Visual Delta (Before vs After)

### 2.1 Baseline State (Before Modification)
- **Current Behavior / Defect**: Mô tả chi tiết giao diện hiện tại của màn hình trước khi sửa (ví dụ: quay số khi không có số may mắn vẫn kích hoạt quay giả; tab mã số may mắn luôn hiển thị kể cả khi đợt bị tắt).
- **Existing HTML / Component Structure**: Cấu trúc layout DOM gốc được trích xuất từ mã nguồn thực tế.

### 2.2 Proposed State (After Modification)
- **Proposed Behavior**: Giao diện sau khi sửa đáp ứng 100% FR trong SRS.
- **Visual Changes (Delta)**:
  - **Added (Thêm mới)**: Các modal, banner, badge, hoặc nút bấm mới (ví dụ: Modal cảnh báo "Chưa có số may mắn hợp lệ trong đợt này để quay thưởng").
  - **Modified (Sửa đổi)**: Nút bấm bị vô hiệu hóa (disabled), thay đổi nhãn, icon trạng thái.
  - **Removed / Hidden (Ẩn / Bỏ)**: Ẩn tab mã số may mắn khi cấu hình tắt đợt, loại bỏ màn hình trùng lặp.

---

## 3. Screen Inventory & Requirement Traceability

| Screen / Component | Target File | Mapped FR-xxx | Before State | After State |
|---|---|---|---|---|
| Booth Lucky Draw | `frontend/src/pages/BoothScreenPage.tsx` | `FR-001`, `FR-002` | Cho phép quay số giả khi danh sách rỗng | Vô hiệu hóa nút quay, hiển thị modal cảnh báo lỗi từ server |
| Draw Card Page | `frontend/src/pages/DrawPage.tsx` | `FR-003` | Luôn hiển thị tab mã may mắn | Ẩn tab số may mắn khi đợt tắt cấp số |

---

## 4. 4-State Behavior Matrix

| State | Interactive Trigger | Visual Representation on Real Screen |
|---|---|---|
| **Normal / Success** | Mặc định hoặc bấm `[Normal]` | Màn hình hiển thị đầy đủ dữ liệu thực tế, các nút bấm hoạt động bình thường, mã trúng thưởng hiển thị chuẩn từ API. |
| **Empty** | Bấm `[Empty]` | Danh sách chưa có dữ liệu, hiển thị placeholder minh họa và CTA hướng dẫn người dùng. |
| **Loading / Skeleton** | Bấm `[Loading]` | Skeleton loading bảo toàn layout gốc của màn hình trong lúc chờ API. |
| **Error / Validation** | Bấm `[Error]` | Modal popup hoặc banner cảnh báo lỗi xuất hiện trực tiếp trên màn hình với thông điệp rõ ràng và nút đóng/thử lại. |

---

## 5. Responsive Breakpoints & Viewport Rules
- **Desktop (1280px)**: Layout đa cột, căn giữa theo tỷ lệ khung nhìn chuẩn, thanh công cụ cố định.
- **Mobile (375px)**: Reflow đơn cột, kích thước nút cảm ứng $\ge 44 \times 44\text{ px}$, không bị tràn ngang.

---

## 6. Accessibility & Contrast Floor
- **WCAG 2.1 AA**: Độ tương phản chữ thường $\ge 4.5:1$, tiêu đề $\ge 3:1$.
- **Focus Rings**: Các phần tử tương tác đều có viền `focus:ring` rõ ràng khi điều hướng bằng bàn phím.
