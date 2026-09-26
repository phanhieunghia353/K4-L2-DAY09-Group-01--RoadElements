# Ontology + CVAT setup

Bảng ontology là **source of truth** cho schema CVAT: `03_cvat_labels.json` phải khớp từng dòng ở đây.

## Ontology table

| Name | Geometry | Type (class / attribute) | Allowed values | Default | Mutable? | Rationale |
|---|---|---|---|---|---|---|
| `traffic_sign` | rectangle | class | — | — | false | Đối tượng biển báo giao thông chính thể hiện trên mặt ảnh, có ranh giới bbox độc lập. |
| `relevance` | — | attribute | `__undefined__`, `relevant`, `not_relevant`, `unknown` | `__undefined__` | false | Thuộc tính cốt lõi của bài toán downstream: Xác định biển báo có hiệu lực trực tiếp khống chế hành vi xe ego hay không. Mặc định `__undefined__` để buộc annotator phải quyết định. |
| `sign_family` | — | attribute | `__undefined__`, `prohibitory`, `mandatory`, `danger`, `other`, `unknown` | `__undefined__` | false | Phân nhóm biển ở cấp cao theo hình dáng/màu sắc (cấm, hiệu lệnh, nguy hiểm, khác, không rõ), giúp mô hình downstream nhận diện nhóm chức năng ngay cả khi ký hiệu chi tiết mờ. |
| `sign_class` | — | attribute | `__undefined__`, 43 class GTSDB, `unknown` | `__undefined__` | false | Mã biển chi tiết chuẩn GTSDB (00 đến 42 hoặc unknown khi bị che/xa không đọc được số hoặc icon). |
| `readable` | — | attribute | `uncertain`, `yes`, `no` | `uncertain` | false | Đánh giá chất lượng thị giác của biển: có đọc được nội dung/số/icon bằng mắt người ở kích thước gốc hay không. Mặc định `uncertain`. |
| `truncated` | — | attribute | `false` (checkbox) | `false` | false | Đánh dấu biển bị mép ảnh cắt mất một phần nhưng vẫn nhận ra họ biển (guideline mục 4.4 và 6.3); box vẽ bám mép ảnh. |
| `needs_review` | — | attribute | `false` (checkbox) | `false` | false | Đánh dấu ca biên mơ hồ cần thảo luận hoặc QA kiểm tra lại trước khi phê duyệt. |
| `image_escalate` | tag | class (tag) | — | — | false | Nhãn cấp ảnh khi bối cảnh giao thông có xung đột biển báo bất thường không thể phân xử hoặc vi phạm điều kiện an toàn downstream. |

## Class hay attribute

- **`traffic_sign` là class:** Vì đây là một thực thể vật lý độc lập (physical object instance) trên mặt đường có bounding box cụ thể.
- **`relevance`, `sign_family`, `sign_class`, `readable`, `truncated`, `needs_review` là attributes:**
  - Nếu tách thành nhiều class (ví dụ `traffic_sign_relevant_speed50`, `traffic_sign_not_relevant_speed50`...) thì số lượng class sẽ bùng nổ tổ hợp (> 250 class), khiến annotator mất nhiều thời gian tìm kiếm trên CVAT UI và dễ click nhầm.
  - Tách thành các trường thuộc tính giúp quy trình gán nhãn mạch lạc: Vẽ box -> Gán họ biển -> Gán class -> Đánh giá relevance cho ego.
- **Default value và nguy cơ bias:**
  - Mặc định cho `relevance`, `sign_family`, và `sign_class` được đặt là `__undefined__`. Nếu đặt mặc định là `relevant` hoặc `prohibitory`, người gán nhãn khi vội hoặc quên chọn sẽ tạo ra lỗi sai âm thầm (silent defect) làm méo mó phân phối dữ liệu huấn luyện. Để `__undefined__` sẽ dễ dàng lọc và bắt lỗi ở bước QC tự động.
  - `readable` mặc định là `uncertain`, buộc annotator phải chủ động xác nhận `yes` (đọc rõ) hoặc `no` (không thể đọc được).

## CVAT

- **Phiên bản CVAT:** CVAT v2.75.1 (chạy local qua Docker tại `http://localhost:8888`)
- **Tên task calibration:** `group1-calib-toan` (task id 30 trên CVAT của Toàn; mỗi thành viên tạo task riêng `group1-calib-<tên>`)
- **Guide của task đã dán `02_guideline.md`?** Có (dán toàn bộ nội dung Markdown của guideline vào mục Guide của task trên CVAT).
- **Nhóm dùng Track hay Shape, vì sao:** Dùng **Shape** (Rectangle). Vì tập dữ liệu GTSDB là các ảnh chụp đơn lẻ tĩnh (single frames độc lập từ các địa điểm khác nhau), không phải chuỗi video liên tục, nên không có sự dịch chuyển hay kế thừa trạng thái giữa các frame.

## Setup test

Thành viên test task: **Nguyễn Thái Dương** (chưa tham gia tạo task ban đầu).
- **Kết quả kiểm tra:**
  1. Label `traffic_sign` hiển thị đúng màu xanh lam, vẽ được hình chữ nhật ôm sát biển.
  2. Bảng attributes hiển thị đầy đủ: `relevance` đứng đầu, tiếp theo là `sign_family`, `sign_class`, `readable`, `truncated`, `needs_review`.
  3. Giá trị mặc định `__undefined__` cảnh báo rõ ràng khi chưa chọn thuộc tính.
  4. Tag `image_escalate` gắn được cho ảnh khi gặp ca xung đột.
- **Vấn đề vấp phải và khắc phục:** Ban đầu danh sách 43 `sign_class` khá dài, gây mất thời gian tìm kiếm nếu chỉ dùng chuột. Nhóm đã bổ sung hướng dẫn trong Guideline: sử dụng phím tắt và chế độ **Attribute Annotation Mode** trên CVAT để gõ lọc nhanh hoặc dùng phím số.
