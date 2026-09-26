# Edge-case library

Tối thiểu 8 card, bao gồm đầy đủ tính đa dạng: occlusion, small_far, ambiguity, conflict, critical, negative, escalation.

---

CASE ID: EC-01
Sample: GTS01
Scene: Đường đôi ngoại ô ban ngày
Observation: Cột bên phải và cột bên trái đều treo 3 biển báo xếp dọc (đường trơn trượt, tốc độ 50, cấm vượt).
Decision: LABEL
Expected: Vẽ 3 bounding box độc lập cho 3 biển trên cột, không vẽ box chung. Cả 3 biển đều gán `relevance = relevant`.
Rationale: Downstream model cần nhận diện từng đối tượng độc lập và áp dụng đồng thời cả 3 giới hạn (giảm tốc, chú ý trơn, không vượt).
Common mistake: Vẽ 1 box to bao trọn cả cụm 3 biển và thân cột.
Diversity: conflict

---

CASE ID: EC-02
Sample: GTS04
Scene: Đường cao tốc liên tỉnh ban ngày
Observation: Cột bên phải có biển giới hạn tốc độ `08 speed limit 120` và biển `10 no overtaking (trucks)` cấm xe tải vượt.
Decision: LABEL
Expected: Vẽ 2 box riêng biệt. Biển tốc độ 120 gán `relevance = relevant`. Biển cấm xe tải vượt gán `relevance = not_relevant`.
Rationale: Xe ego là xe con chở khách tiêu chuẩn, không thuộc đối tượng xe tải nên không bị cấm vượt; nếu đánh nhãn relevant, xe ego sẽ từ chối vượt xe an toàn.
Common mistake: Đánh nhãn `relevance = relevant` cho biển cấm xe tải vì thấy cắm trên làn xe chạy.
Diversity: critical

---

CASE ID: EC-03
Sample: GTS09
Scene: Đường đô thị có dải phân cách và đảo giao thông
Observation: Biển tròn xanh mũi tên trắng `38 keep right` cắm trên mũi đảo tam giác phân làn bên trái hướng đi của xe.
Decision: LABEL
Expected: 1 bounding box ôm khít mặt biển tròn, `relevance = relevant`, `sign_family = mandatory`, `sign_class = 38 keep right`.
Rationale: Mặc dù cắm trên đảo phân cách phía bên trái, biển có hiệu lực bắt buộc xe ego phải giữ làn đi về phía bên phải của đảo.
Common mistake: Tưởng biển cắm bên trái là dành cho làn ngược chiều nên đánh nhãn `not_relevant`.
Diversity: edge

---

CASE ID: EC-04
Sample: GTS07
Scene: Đường quốc lộ nông thôn, cảnh quan trống trải
Observation: Không có bất kỳ biển báo giao thông nào xuất hiện trong toàn bộ khung hình.
Decision: IGNORE
Expected: Không vẽ bất kỳ bounding box nào (0 annotation).
Rationale: Kiểm tra tính nghiêm ngặt của mô hình và người gán nhãn, triệt tiêu lỗi tạo False Positive (nhìn nhầm bóng râm hoặc ngọn cây thành biển).
Common mistake: Cố tìm và vẽ box vào các vật thể tròn/tam giác không phải biển báo.
Diversity: negative

---

CASE ID: EC-05
Sample: GTS06
Scene: Đường phố ban ngày, biển ở cự ly xa
Observation: Một biển giới hạn tốc độ cắm bên phải đường nhưng kích thước nhỏ do khoảng cách xa (< 25x25 px).
Decision: LABEL
Expected: Vẽ box ôm khít biển, gán `sign_family = prohibitory`, `readable = no`, `sign_class = unknown`, `relevance = relevant`.
Rationale: Nhìn rõ hình tròn viền đỏ chứng tỏ là biển cấm khống chế làn, nhưng không thể đọc rõ con số; tuyệt đối không đoán mò số 30 hay 50.
Common mistake: Tự phỏng đoán con số `01 speed limit 30` khi mắt người không thể đọc rõ nét số.
Diversity: small_far

---

CASE ID: EC-06
Sample: GTS10
Scene: Giao lộ có 2 biển hiệu lệnh cùng loại 33 go right ở 2 vị trí khác nhau
Observation: Hai biển hiệu lệnh rẽ phải 33 go right xuất hiện trong cùng khung cảnh: một biển cắm bên phải làn tiếp cận ngã rẽ và một biển cắm ở góc phía xa đối diện.
Decision: LABEL
Expected: Vẽ 2 box riêng cho 2 biển. Biển cắm trực tiếp bên phải làn tiếp cận đón đầu ego gán relevance = relevant; biển cắm ở góc đối diện/phía xa gán relevance = not_relevant.
Rationale: Biển cùng loại sign_class nhưng relevance quyết định theo vị trí không gian tương quan với làn của ego, không suy diễn theo loại biển.
Common mistake: Mặc định gán cùng một giá trị relevance cho cả hai biển chỉ vì chúng cùng chung một mã sign_class.
Diversity: conflict

---

CASE ID: EC-07
Sample: GTS22
Scene: Ngã tư giao cắt lớn có đảo giao thông
Observation: Hai biển `14 stop` cắm ở cả hai bên ngã tư (bên phải và bên trái), kèm 1 biển `38 keep right` trên đảo giao thông.
Decision: LABEL
Expected: Vẽ 3 box riêng biệt. Cả 2 biển STOP đều gán `relevance = relevant`. Box biển STOP ôm khít mép bát giác đỏ.
Rationale: Biển STOP khống chế toàn bộ luồng phương tiện tiến vào ngã tư; việc cắm hai bên đường là để đảm bảo tầm nhìn tối đa cho tài xế/cảm biến.
Common mistake: Chỉ dán nhãn biển STOP bên phải và bỏ quên biển STOP bên trái; hoặc đánh nhãn `not_relevant` cho biển bên trái.
Diversity: critical

---

CASE ID: EC-08
Sample: GTS21
Scene: Vùng núi tuyết, điều kiện thời tiết phức tạp
Observation: Một biển nguy hiểm có biểu tượng bông tuyết `30 snow` rất lớn ở cự ly gần bên phải, và một biển giao cắt ưu tiên `11 priority at next intersection` rất nhỏ, mờ ở xa bên trái.
Decision: LABEL
Expected: Biển tuyết: `relevant`, `sign_class = 30 snow`, `readable = yes`. Biển nhỏ ở xa: `sign_family = danger`, `sign_class = unknown`, `readable = no`, `relevance = unknown`, bật `needs_review = true`.
Rationale: Biển nhỏ ở xa không đủ bằng chứng hình ảnh để xác định chắc chắn làn áp dụng và loại giao cắt, cần đưa vào luồng kiểm tra review.
Common mistake: Đánh nhãn `readable = yes` cho biển ở xa dù không nhìn rõ biểu tượng tam giác.
Diversity: escalation
