# User Requirements Document (URD) — Cột Mốc

**Tên dự án:** Cột Mốc (`cot-moc`)
**Mục tiêu:** Ứng dụng di động dành cho người đi phượt kết hợp **an toàn sinh tồn (SOS & theo dõi hành trình khi mất sóng)** và **nhật ký hành trình (check-in ảnh, tô màu tỉnh thành, chia sẻ cung đường)**.
**Tech Stack:**
- **Mobile App:** React Native (TypeScript, Offline-first local storage).
- **Backend & Web Tracking:** FastAPI (Python), cung cấp REST API đồng bộ dữ liệu, gửi cảnh báo đa kênh và trang web nhẹ để người thân xem vị trí SOS trực tiếp.

---

## Phạm vi Phase 1 (MVP) — Chạy Run đầu tiên

### 1. Tài khoản & Hồ sơ khẩn cấp
- **REQ-001 (Đăng ký / Đăng nhập):** Người dùng đăng ký, đăng nhập bằng số điện thoại hoặc email; phiên đăng nhập lưu an toàn trên thiết bị.
- **REQ-002 (Danh bạ người thân khẩn cấp):** Người dùng thêm/sửa/xóa tối đa 5 liên hệ khẩn cấp (Tên, SĐT, Mối quan hệ).
- **REQ-003 (Thẻ thông tin y tế & xe):** Người dùng lưu sẵn nhóm máu, dị ứng thuốc, bệnh nền, biển số xe và loại xe để đính kèm khi phát SOS.

### 2. An toàn & Cảnh báo khẩn cấp (Core SOS)
- **REQ-004 (Nút SOS khẩn cấp 1 chạm):** Màn hình chính có nút SOS nổi bật (yêu cầu bấm giữ 3 giây để kích hoạt, kèm đếm ngược 5 giây cho phép hủy nếu bấm nhầm).
- **REQ-005 (Cảnh báo đa kênh & SMS Fallback):**
  - Khi có mạng: App gửi tín hiệu SOS lên FastAPI backend để phát Push Notification / thông báo tới người thân kèm tọa độ GPS, mức pin, thời điểm cập nhật cuối và link Web theo dõi.
  - Khi mất mạng (Offline): App tự động chuyển sang mở/gửi tin nhắn SMS chứa tọa độ GPS (dạng link Google Maps) + % pin + thông tin khẩn cấp tới danh bạ người thân.
- **REQ-006 (Trang Web theo dõi trực tiếp cho người thân):** FastAPI cung cấp một URL công khai theo mã phiên (token tạm thời) hiển thị vị trí cuối cùng, trạng thái SOS, mức pin và vệt di chuyển gần nhất mà người thân không cần cài app.
- **REQ-007 (Hẹn giờ Check-in an toàn — Dead Man's Switch):** Người dùng đặt mốc thời gian dự kiến an toàn (ví dụ 18:00). Nếu quá giờ mà không bấm "Tôi an toàn", hệ thống tự động phát cảnh báo kèm tọa độ cuối cùng cho người thân.
- **REQ-008 (Lưu vết hành trình nền — Breadcrumb Trail):** Khi bật chế độ "Bắt đầu chuyến đi", app ghi nhận tọa độ GPS theo chu kỳ tối ưu pin (giảm tần suất khi đứng yên), lưu cục bộ và đồng bộ lên server khi có mạng.

### 3. Nhật ký hành trình & Chia sẻ (Trip Journal)
- **REQ-009 (Quản lý chuyến đi):** Người dùng bấm Bắt đầu / Tạm dừng / Kết thúc chuyến đi; xem lại danh sách các chuyến đi đã thực hiện kèm tổng quãng đường (`km`) và thời gian di chuyển.
- **REQ-010 (Check-in & Ghi chú trên bản đồ):** Trong chuyến đi, người dùng chụp ảnh + nhập ghi chú gắn đúng vị trí GPS hiện tại. Nếu đang mất sóng, ảnh và ghi chú được lưu vào hàng đợi cục bộ (offline queue) và tự đồng bộ khi có mạng.
- **REQ-011 (Watermark thông số lên ảnh Check-in):** Ảnh chụp/check-in được gắn watermark gồm: Tên địa điểm (hoặc tọa độ), Độ cao (`m`), và Ngày giờ chụp.
- **REQ-012 (Export ảnh hành trình để khoe):** Người dùng chọn 2–4 ảnh check-in nổi bật và tùy chọn ẩn 1–2 km đầu/cuối (che địa chỉ riêng), xuất ra ảnh tổng kết (Poster 9:16 hoặc 1:1) gồm cung đường đã vẽ + ảnh check-in + tổng `km` + thời gian để lưu về máy hoặc chia sẻ mạng xã hội.

---

## Phạm vi Phase 2 (Mở rộng sau MVP)

### 4. Tiện ích sinh tồn & Bản đồ Offline
- **REQ-013 (Tải gói Offline theo cung đường):** Tải sẵn bản đồ khu vực và dữ liệu cứu hộ trước khi vào vùng mất sóng.
- **REQ-014 (Danh bạ cứu hộ & Sửa xe dọc tuyến Offline):** Tra cứu SĐT đội cứu hộ, tiệm sửa xe/vá lốp, trạm y tế gần vị trí GPS hiện tại nhất khi không có mạng; có nút xác nhận từ cộng đồng ("vừa gọi được" / "không liên lạc được").
- **REQ-015 (Bản đồ cây xăng & Điểm nghỉ):** Hiển thị trạm xăng và điểm nghỉ dọc tuyến, cảnh báo đoạn đường dài không có cây xăng.

### 5. Khám phá & Hồ sơ Phượt thủ
- **REQ-016 (Tự động tô màu tỉnh thành Offline):** Dùng dữ liệu ranh giới hành chính chạy offline trên máy để tự đánh dấu các tỉnh thành đã đi qua (có lọc nhiễu khi đi sát ranh giới).
- **REQ-017 (Bản đồ kỷ niệm theo tỉnh):** Bấm vào từng tỉnh đã tô màu để xem lại ảnh check-in và các chuyến đi qua tỉnh đó.
- **REQ-018 (Profile thống kê thành tích):** Hiển thị tổng `km` đã chạy, số tỉnh đã tô màu (`x/63`), đỉnh đèo/độ cao cao nhất từng qua, tổng số ngày trên đường.
