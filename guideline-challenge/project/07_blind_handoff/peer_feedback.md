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
| Feedback 2 + 3: biển chỉ hướng/địa danh (route number, tên thị trấn) ở GTS21 không rõ in/out scope | guideline gap | accept + revise: mục 1 và bảng mục 5 quy định rõ mọi biển chỉ dẫn hướng/địa danh/route number, bất kể màu nền, là IGNORE; thêm GTS21 làm ví dụ ở v3 | Peer nêu GTS21 và đã gán một box cho cụm bảng; v2 nêu bảng xanh/khoảng cách nhưng ví dụ chưa bao quát cụm panel vàng/trắng |
| Feedback 4: `readable` mặc định `uncertain`, CVAT không ép chọn | guideline gap (thiết kế default) | accept + revise: v3 nhắc annotator chủ động chọn `readable` trên từng object; giữ nguyên labels JSON/task đã freeze cho blind này. Chỉ đổi default trước freeze của lần chạy tiếp theo | `03_cvat_labels.json` đã gửi peer: `readable` kiểu radio có `default_value=uncertain`; peer phản ánh rủi ro bỏ quên giá trị này |
| Feedback 5: thêm 1 câu về biển chỉ hướng | guideline gap | accept + revise (gộp với feedback 2 + 3) | Như trên |
| 11 dòng chấm 0 có note `gold sai:` (GTS22 d1–d4; GTS18 d1; GTS14 d1–d2; GTS21 d1–d2; GTS26 d1–d2) | execution error của owner: gold và mô tả `sample_pack.csv` cho các blind ảnh không khớp ảnh gốc | Chấm 0 theo frozen gold và ghi `gold sai:` như quy trình yêu cầu; không sửa gold/sample pack sau freeze. Không suy ra guideline kém từ những dòng này; đánh giá các lỗi peer độc lập riêng ở các hàng dưới. Cải tiến lần sau: hai người đối chiếu toàn bộ gold với ảnh gốc trước freeze, lưu tọa độ box và checklist theo sample | Ảnh blind trong export khớp ID với `data/gtsdb`. GTS22 không có STOP; GTS18 có 21 + 01, không có 17; GTS14 chỉ có 11; GTS21 có 27 + 39 cùng cụm chỉ đường, không có 30; GTS26 chỉ có 21. Xem từng dòng `gold sai:` trong `transfer_score.csv` |
| Peer gán `sign_family=danger` cho class 13 give way (GTS22) và class 11 priority at next intersection (GTS14) | guideline gap (quy tắc family cần được nêu nổi bật hơn) | accept + revise: mục 4.2 và Common mistakes nêu riêng class 13 và 11 thuộc `other`, không suy family chỉ từ hình tam giác | Peer export `Mixigaming-blind.zip`; class 13/11 và family peer đã chọn ghi trong `transfer_score.csv` |
| Peer vẽ cụm biển chỉ hướng GTS21; đồng thời vẽ bảng địa danh và chevron ngoài taxonomy ở GTS22 | guideline gap cho cụm chỉ hướng GTS21; execution error cho các vật thể ngoài taxonomy ở GTS22 | GTS21: accept + revise, ghi rõ panel chỉ hướng bất kể màu nền phải IGNORE. GTS22: reject quyết định vẽ thêm với bằng chứng, vì quy tắc 43 class và ví dụ biển địa danh đã có ở v2 | Peer export `Mixigaming-blind.zip`; đối chiếu ảnh gốc GTS21/GTS22 và các box trong XML |
