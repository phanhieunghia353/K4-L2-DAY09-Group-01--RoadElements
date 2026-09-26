# Problem statement + downstream contract

Tối đa nửa trang, viết trước khi mở CVAT. Đây là bằng chứng của gate G1 (topic lock). Thay mọi placeholder mới là xong.

## Bài toán

Xác định ranh giới hình học và phân loại mức độ liên quan/hiệu lực thực tế đối với xe tự hành (ego-vehicle relevance) của các biển báo giao thông trên tập dữ liệu đường bộ Đức (GTSDB), giải quyết các tình huống nhập nhằng khi xuất hiện nhiều biển báo cùng lúc trên một cột, biển cắm hai bên đường, biển áp dụng riêng cho loại phương tiện khác (xe tải), hoặc biển báo cắm ở đảo giao thông/đường nhánh.

## Downstream contract

1. **Downstream task / model / user là ai?**
   Hệ thống tự hành L2+/L3 (Mô-đun Nhận diện Biển báo Giao thông kết hợp Lập kế hoạch Di chuyển - Motion Planning & Speed Advisory). Xe tự hành đối tượng là dòng xe con chở khách tiêu chuẩn (standard passenger car).

2. **Output annotation nào thực sự cần?**
   - **Geometry:** Bounding box (`rectangle`) bao khít mặt hiển thị của biển báo (không bao gồm cột đỡ hay phụ kiện giá treo).
   - **Taxonomy:** `sign_family` (prohibitory, mandatory, danger, other, unknown) và `sign_class` (43 mã biển GTSDB hoặc unknown).
   - **Ego-relevance:** `relevance` (`relevant`, `not_relevant`, `unknown`) xác định xem biển có bắt buộc ego phải tuân thủ hành vi hay không.
   - **Quality & Escalation:** `readable` (`yes`, `no`, `uncertain`), `truncated` (boolean), `needs_review` (boolean), và tag mức ảnh `image_escalate`.

3. **Failure nào gây hậu quả lớn nhất? (Critical errors trong gold):**
   - **Bỏ sót hoặc đánh nhãn sai `not_relevant` cho biển cấm/dừng có hiệu lực trực tiếp:** Điển hình là biển `14 stop`, `17 no entry`, `13 give way`, hoặc biển tốc độ giới hạn thấp (`speed limit 20/30/50`) áp dụng cho làn của ego. Hậu quả: Xe không dừng hoặc không giảm tốc, gây nguy cơ va chạm trực diện hoặc đi vào đường cấm/ngược chiều.
   - **Đánh nhãn nhầm `relevant` cho biển không áp dụng cho ego:** Đánh nhãn `relevant` cho biển chỉ áp dụng cho xe tải (`10 no overtaking (trucks)`, `16 no trucks`), hoặc biển cắm riêng cho làn rẽ nhánh phụ mà ego không đi vào. Hậu quả: Xe phanh gấp bất ngờ (phantom braking) hoặc từ chối vượt xe an toàn, gây cản trở giao thông và nguy cơ bị đâm từ phía sau.

4. **Khi ambiguity không resolve được, ai / ở đâu là escalation path?**
   - Khi biển bị che khuất một phần lớn, quá xa, hoặc bối cảnh làn đường không đủ bằng chứng để khẳng định biển có hiệu lực với ego: Annotator chọn `relevance = unknown` và bật checkbox `needs_review = true`.
   - Khi phát hiện tình huống xung đột giao thông nghiêm trọng (ví dụ 2 biển ngược nghĩa trên cùng làn) hoặc cảnh chụp không thể phân xử theo luật: Annotator gắn nhãn tag `image_escalate` cho ảnh, ghi chú cụ thể để Tech Lead / Domain Expert xử lý.

## Scope

- **Trong scope (bắt buộc label):** Mọi biển báo giao thông thuộc 4 nhóm (cấm, hiệu lệnh, nguy hiểm, khác) có mặt trước hướng về phía xe ego (nhìn thấy được mặt biển hoặc ký hiệu) với kích thước tối thiểu >= 10x10 pixels. Bao gồm biển bên phải, bên trái, trên giá long môn và trên đảo giao thông.
- **Ngoài scope (ignore):**
  - Mặt sau của biển báo quay về hướng ngược lại (không thấy ký hiệu mặt biển).
  - Biển báo bị che khuất hoàn toàn (100%).
  - Biển báo phụ tư nhân, biển quảng cáo, biển tên đường nhỏ, biển số nhà không thuộc quy chuẩn đường bộ.
  - Biển quá nhỏ (< 10x10 pixels) hoặc mờ nhòe tới mức không thể xác định được hình dạng hình học.
- **Geometry tolerance:** Bounding box ôm sát viền ngoài cùng của mặt biển hiển thị (tight bounding box), dung sai <= 3 px ở mỗi cạnh. Tuyệt đối không lấy cột đỡ, giá treo hoặc khoảng trống nền trời.

## Output chấm được

Mọi quyết định đều hiển thị tường minh trong file xuất CVAT (`annotations.xml`):
- Quyết định hình học: Box ôm khít viền mặt biển (<= 3 px tolerance).
- Quyết định phân loại: Đúng `sign_family` và `sign_class`.
- Quyết định hiệu lực: Đúng `relevance` (`relevant`, `not_relevant`, `unknown`).
- Quyết định trạng thái: `readable` (`yes`, `no`, `uncertain`), cờ `truncated`, cờ `needs_review`, và tag `image_escalate`.

## Dữ liệu và giới hạn

- **Nguồn dữ liệu:** 28 ảnh GTSDB chuẩn (`data/gtsdb/GTS01.png` đến `GTS28.png`), kích thước 1360 x 800 px.
- **Giới hạn đã biết:** Dữ liệu là ảnh tĩnh (single frame), giao thông Đức (Công ước Vienna, tay lái bên phải đường). Có các ảnh âm tính (negative samples: `GTS07`, `GTS24`) không có bất kỳ biển báo nào để kiểm tra khả năng không sinh False Positive của người gán nhãn.
