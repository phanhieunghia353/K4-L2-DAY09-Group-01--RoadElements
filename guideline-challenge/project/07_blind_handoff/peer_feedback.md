# Peer feedback + owner response

Phần 1 do **nhóm peer** trả lời (gửi kèm file export). Phần 2 do **nhóm owner** điền. Thay mọi placeholder mới
là xong (gate G5).

- **Nhóm peer:** Mixigaming
- **Người label blind:** Cẩm Vũ Ngọc Thạch

## 1. Peer trả lời

1. Rule nào rõ nhất / giúp quyết định nhanh nhất?
   Mục 4.1 relevance với ví dụ cụ thể (biển bên phải khống chế làn ego, biển trên đảo giao thông, cặp biển đối xứng hai bên) — nhờ có ví dụ số hiệu rõ ràng (38 keep right, 39 keep left...) nên với biển đứng riêng lẻ, quyết định relevant/not_relevant rất nhanh, gần như không phải suy nghĩ (ví dụ GTS18: 2 biển cùng cột trên đường 1 chiều, chọn relevant ngay).
2. Rule nào mơ hồ hoặc phải tự suy diễn?
   Guideline liệt kê 4 nhóm sign_family (prohibitory/mandatory/danger/other) nhưng không nói rõ biển chỉ dẫn địa danh/hướng đi (biển tên đường, biển route number) có tính là "trong scope" hay không — mục 1 chỉ loại trừ "biển tên đường nhỏ", còn cụm biển chỉ hướng lớn (kiểu bảng chỉ dẫn cao tốc/thị trấn) thì không thấy nhắc tới, cũng không khớp gọn vào family nào trong 4 family liệt kê. Phải tự suy diễn có nên vẽ hay bỏ qua.
3. Sample nào khiến guideline "vỡ"?
   GTS21 — ảnh có cụm 3 biển chỉ hướng địa danh (route number + tên thị trấn) cắm cùng cột bên trái. Không có rule nào trong guideline nói rõ loại biển này thuộc sign_family nào hay có nằm trong scope không, nên không thể tự tin gán nhãn mà không đoán.
4. Attribute / default nào trong CVAT dễ gây thao tác sai?
   readable có default là uncertain (không phải __undefined__ như các attribute khác) — điều này dễ khiến annotator quên bấm chọn vì CVAT không báo thiếu (không giống relevance/sign_family/sign_class có __undefined__ ép chọn). Annotator vội có thể để nguyên uncertain cho biển thực ra đọc rất rõ, làm sai lệch dữ liệu mà không ai phát hiện lúc export.
5. Một thay đổi cụ thể giúp annotator mới ít hỏi hơn?
   Thêm 1 dòng vào mục 1 (Scope) hoặc mục 5 (Inclusion/exclusion) nói rõ: "Biển chỉ dẫn địa danh/hướng đi (route number, tên thị trấn) — IGNORE, không thuộc 4 family chuẩn" hoặc ngược lại nếu nhóm owner muốn tính vào thì cần thêm 1 giá trị sign_family mới cho loại này. Chỉ cần 1 câu là giải quyết được điểm mơ hồ lớn nhất gặp phải.

## 2. Owner phân loại

Owner không tranh luận để bảo vệ guideline. Mỗi feedback và mỗi decision peer làm sai được xếp vào một hướng xử lý.

| Feedback / decision sai | Nguyên nhân (guideline gap / data ambiguity / execution error) | Xử lý (accept + revise / reject with evidence / add escalation rule) | Bằng chứng |
|---|---|---|---|
| Feedback 1: mục 4.1 relevance + ví dụ số hiệu giúp quyết nhanh | — (điểm mạnh) | Giữ nguyên ở v3 | Peer gán relevant đúng cho mọi biển thật ở 5 ảnh blind |
| Feedback 2 + 3: biển chỉ hướng/địa danh (route number, tên thị trấn) ở GTS21 không rõ in/out scope | guideline gap | accept + revise: mục 1 và bảng mục 5 đổi định nghĩa từ "bảng xanh to, khoảng cách km" sang "mọi biển chỉ dẫn hướng/địa danh/route number, bất kể màu nền (xanh, vàng, trắng)" → IGNORE, thêm GTS21 làm ví dụ ở v3 | `02_guideline.md` dòng 19 và 95 chỉ mô tả bảng xanh có km; GTS21 là cụm biển vàng/trắng có số route màu xanh; peer vẽ box và gán `sign_family=other`, trái với lưu ý dòng 71 |
| Feedback 4: `readable` mặc định `uncertain`, CVAT không ép chọn | guideline gap (thiết kế labels JSON) | accept + revise: thêm `__undefined__` làm giá trị đầu tiên và mặc định của `readable` trong labels JSON v3 | `03_cvat_labels.json`: `readable` kiểu radio, `default_value = uncertain`; các select khác đều mặc định `__undefined__` |
| Feedback 5: thêm 1 câu về biển chỉ hướng | guideline gap | accept + revise (gộp với feedback 2 + 3) | Như trên |
| 10 decision chấm 0 có note `gold sai:` (GTS22 d2, d3, d4; GTS18 d1; GTS14 d1, d2; GTS21 d1, d2; GTS26 d1, d2) | execution error của owner: gold và mô tả `sample_pack.csv` cho 5 ảnh blind được viết mà không mở ảnh gốc để đối chiếu | accept (peer đúng theo ảnh thật); không sửa gold đã freeze. Revise quy trình: gold v3 phải kèm tọa độ box đo trên ảnh gốc và một người thứ hai mở ảnh xác nhận trước khi freeze | Ảnh gửi đi, `build/blind` và `data/gtsdb` trùng md5. Ảnh thật: GTS22 là biển thông tin + nhường đường 13 + bảng chevron dưới gầm cầu, không có STOP; GTS18 là biển 21 + 01, không có biển 17; GTS14 chỉ có biển 11; GTS21 là 27 + 39 + cụm chỉ hướng, không có biển 30; GTS26 chỉ có biển 21 |
| Peer gán `sign_family=danger` cho biển 13 give way (GTS22) và biển 11 priority at next intersection (GTS14); không được chấm vì gold không có decision này | guideline gap | accept + revise: mục 4.2 thêm câu "biển tam giác ưu tiên/nhường đường là `other` dù có hình tam giác viền đỏ", kèm ví dụ | `02_guideline.md` dòng 71 xếp give way và priority at next intersection vào `other`, nhưng rule này nằm lẫn trong một câu dài; peer phân theo hình dạng tam giác |
