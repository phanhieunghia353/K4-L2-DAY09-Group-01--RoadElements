# Annotation guideline — Xác định Biển báo Giao thông & Mức độ Liên quan tới Xe Tự hành (Ego-Relevance)

**Version:** v3

Tài liệu này là quy chuẩn hướng dẫn gán nhãn cho dự án Nhận diện & Đánh giá Hiệu lực Biển báo Giao thông đối với xe tự hành (Ego Vehicle) trên bộ dữ liệu GTSDB. Người gán nhãn phải tuân thủ nghiêm ngặt các quy tắc dưới đây mà không dựa vào phỏng đoán cá nhân.

---

## 1. Objective + scope

- **Mục tiêu:** Cung cấp dữ liệu huấn luyện cho hệ thống lái xe tự hành L2+/L3 (Module ADAS Motion Planning & Speed Advisory). Xe tự hành mục tiêu là **xe con chở khách tiêu chuẩn (standard passenger car)**. Mô hình cần biết:
  1. Vị trí chính xác của từng biển báo phía trước.
  2. Loại biển báo (cấm, hiệu lệnh, nguy hiểm, cảnh báo).
  3. **Biển báo đó có bắt buộc xe ego phải tuân thủ hành vi hay không (`relevance`)**.
- **Phạm vi trong scope (bắt buộc gán nhãn):**
  - Mọi biển báo giao thông thuộc đúng **danh mục 43 class chuẩn của GTSDB** (các nhóm prohibitory, mandatory, danger, other) hướng mặt về phía xe (nhìn thấy được mặt trước hoặc biểu tượng) có kích thước >= 10x10 pixels.
  - Bao gồm biển cắm bên phải đường, bên trái đường, trên dải phân cách giữa/đảo giao thông, và trên giá long môn.
- **Phạm vi ngoài scope (bỏ qua - IGNORE, TUYỆT ĐỐI KHÔNG VẼ BOX):**
  - **Biển chỉ dẫn hướng đi, địa danh, số tuyến đường:** IGNORE bất kể màu nền xanh, vàng hay trắng; gồm bảng chỉ hướng, biển tên thành phố/thị trấn, ký hiệu route number và cụm nhiều panel trên cùng cột (ví dụ cụm chỉ đường trong `GTS21`). Các loại này không thuộc 43 class GTSDB.
  - **Biển bãi đỗ xe:** Biển hình vuông xanh lam có chữ P trắng (`Parking`).
  - **Biển đường một chiều:** Biển hình chữ nhật xanh có mũi tên trắng (`Einbahnstraße`).
  - **Biển phụ (Zusatzzeichen):** Các biển phụ chữ nhật nhỏ viền đen chữ đen gắn kèm bên dưới biển chính (ví dụ: mũi tên chỉ hướng rẽ, số mét khoảng cách, giới hạn thời gian...). Biển phụ dùng để tham khảo ngữ cảnh cho biển chính, **không vẽ box riêng cho biển phụ**.
  - Mặt sau của biển báo quay về hướng xe ego (chỉ thấy lưng kim loại hoặc khung đỡ).
  - Biển báo bị che khuất hoàn toàn (100%).
  - Biển quảng cáo, biển tên đường nhỏ, biển số nhà, biển báo công trình tư nhân.
  - Biển quá nhỏ (< 10x10 pixels) hoặc mờ nhòe tới mức mắt người không thể nhận diện được hình dạng hình học.
  - **Quy tắc bao quát:** Mọi biển báo nằm ngoài danh mục 43 class GTSDB đều là **IGNORE (Không vẽ box)**!

---

## 2. Annotation unit

- **Đơn vị gán nhãn:** Ảnh tĩnh độc lập (Single-frame Image).
- **Loại hình học:** Hình chữ nhật độc lập (Instance Bounding Box - 2D Rectangle).
- Mỗi biển báo vật lý là một instance riêng biệt. Nếu trên cùng một cột có nhiều biển báo treo chồng lên nhau, **mỗi biển báo phải được vẽ một bounding box riêng**, không vẽ gộp cả cụm biển vào một box lớn. Biển phụ gắn kèm không vẽ box.

---

## 3. Geometry rule

- **Tight bounding box:** Bounding box phải ôm khít viền mép ngoài cùng của mặt biển hiển thị (visible boundary).
- **Không bao gồm phụ kiện:** Tuyệt đối không kéo box trùm qua cột đỡ, thanh giằng kim loại, giá treo, biển phụ bên dưới hoặc khoảng trống nền trời xung quanh.
- **Biển bị che một phần (Occlusion):** Vẽ box ôm trọn phần nhìn thấy được của mặt biển (visible area). Nếu phần bị che >= 10% diện tích biển nhưng vẫn nhận biết được hình học, bật cờ `needs_review`.
- **Dung sai hình học (Tolerance):** Sai số biên <= 3 pixels ở mỗi cạnh so với mép thực tế của mặt biển.

---

## 4. Taxonomy & Attributes

Mỗi bounding box `traffic_sign` phải được gán đủ các thuộc tính sau (không được để sót `__undefined__`):

### 4.1 Thuộc tính `relevance` (Hiệu lực đối với xe Ego)
Đây là thuộc tính quan trọng nhất cho downstream model:
- **`relevant` (Có hiệu lực / Xe cần để tâm tuân thủ):**
  1. Biển đặt bên phải đường cùng chiều, khống chế trực tiếp làn xe ego đang di chuyển (ví dụ: biển giới hạn tốc độ, biển báo nguy hiểm đường cong, công trường, động vật qua đường).
  2. Biển cắm trên đảo giao thông hoặc dải phân cách trực tiếp phía trước hướng đi của xe (ví dụ: `38 keep right`, `39 keep left`, `40 roundabout`).
  3. Cặp biển cắm đối xứng hai bên đường (cả bên trái và bên phải, như trên cao tốc hoặc đường một chiều) có hiệu lực chung cho toàn bộ các làn xe cùng chiều (ví dụ: cặp biển `08 speed limit 120` ở cả hai bên đường trong `GTS04`, `GTS08`).
  4. Biển `14 stop` hoặc `13 give way` tại giao lộ phía trước mà xe ego chuẩn bị tiến vào.
  5. **Biển tại nút giao phía trước liên quan trực tiếp đến an toàn (Situational Awareness):** Các biển cảnh báo người đi bộ (`27 pedestrian crossing`), biển giới hạn tốc độ thấp (`00 speed limit 20`, `01 speed limit 30`) cắm tại ngã tư phía trước mặt xe ego: Xe bắt buộc phải đưa vào bộ nhớ theo dõi để phòng ngừa người đi bộ tràn ra đường, do đó **vẫn là `relevant`**.
- **`not_relevant` (Vẫn vẽ box thuộc 43 class nhưng KHÔNG áp dụng cho Ego):**
  1. **Biển áp dụng cho phương tiện khác:** Điển hình là các biển chỉ dành riêng cho xe tải như `10 no overtaking (trucks)`, `16 no trucks`, hoặc biển hết hạn chế xe tải `42 restriction ends (overtaking (trucks))`. Vì xe ego là xe con standard, các biển này không khống chế quyền đi hay vượt của ego.
  2. **Biển dành riêng cho làn rẽ hoặc đường nhánh gom tách biệt:** Biển cắm trên nhánh đường phụ/đường gom rẽ nhánh mà xe ego không đi vào (khi ego đang chạy thẳng trên trục đường chính).
  3. **Biển hướng sang hướng đường cắt ngang:** Biển báo cắm phục vụ cho phương tiện ở luồng đường giao cắt mà không áp dụng cho chiều đi của ego.
- **`unknown` (Chưa đủ bằng chứng xác định):**
  - Biển ở quá xa hoặc bị che khuất khiến không thể xác định biển điều khiển làn nào, hoặc giao lộ quá phức tạp mà không có bằng chứng làn đường rõ ràng.

### 4.2 Thuộc tính `sign_family` (Họ biển báo)
- `prohibitory`: Biển báo cấm (hình tròn viền đỏ nền trắng, hoặc viền đỏ có gạch chéo, hoặc biển cấm đi vào).
- `mandatory`: Biển hiệu lệnh bắt buộc (hình tròn nền xanh lam có mũi tên trắng).
- `danger`: Biển cảnh báo nguy hiểm (hình tam giác đều đỉnh hướng lên, viền đỏ nền trắng/vàng).
- `other`: Biển ưu tiên (hình thoi vàng `priority road`, tam giác ngược `13 give way`, bát giác `stop`, tam giác `11 priority at next intersection`), và biển hết hạn chế (`restriction ends` hình tròn nền trắng có vạch chéo xám). Gán theo class GTSDB, không chỉ theo dáng tam giác: class `13` và `11` đều là `other`, dù viền đỏ và hình tam giác. **Tuyệt đối không gán biển chỉ dẫn vuông/chữ nhật vào nhóm này.**
- `unknown`: Không thể nhận diện được hình dạng/màu sắc họ biển.

### 4.3 Thuộc tính `sign_class` (Mã biển chi tiết GTSDB)
Chọn 1 trong 43 mã biển chuẩn từ `00` đến `42` theo danh mục GTSDB. Nếu biểu tượng bên trong bị mờ, lóa hoặc quá xa không đọc được số/icon, chọn `unknown`. Tuyệt đối không đoán mò số khi `readable = no`.

### 4.4 Thuộc tính chất lượng
- `readable`:
  - `yes`: Đọc rõ ràng con số/biểu tượng mặt biển ở tỷ lệ thu phóng 100%.
  - `no`: Nhìn thấy có mặt biển nhưng không thể đọc được nội dung bên trong.
  - `uncertain`: Nửa rõ nửa mờ, phán đoán không chắc chắn.
  - CVAT labels đã freeze cho blind task đặt mặc định là `uncertain`. Đây chỉ là giá trị mặc định thao tác, không phải quyết định đã kiểm tra: annotator phải chủ động chọn `yes`, `no` hoặc `uncertain` cho từng biển.
- `truncated`: Checkbox `true` nếu biển bị mép ảnh cắt mất một phần.
- `needs_review`: Checkbox `true` nếu là ca biên cần xem xét lại.

---

## 5. Inclusion / exclusion

| Trường hợp | Hành động | Thuộc tính | Giải thích |
|---|---|---|---|
| Biển trên cùng cột cắm bên phải đường | LABEL từng biển riêng | Phụ thuộc từng biển | Mỗi biển một box, gán relevance độc lập |
| Biển `10 no overtaking (trucks)` cắm cùng cột biển tốc độ | LABEL cả hai box | Biển tốc độ: `relevant`; biển cấm xe tải: `not_relevant` | Biển xe tải thuộc 43 class nhưng không áp dụng cho xe con ego |
| Biển cắm ở đảo phân làn bên trái (`keep right`) | LABEL | `relevant` | Hướng dẫn xe ego phải đi vòng qua bên phải đảo |
| Biển phụ chữ nhật nhỏ gắn dưới biển chính | **IGNORE (Không vẽ box)** | — | GTSDB không có class cho biển phụ; dùng nó làm ngữ cảnh xét relevance biển chính |
| Biển chỉ dẫn hướng đi/địa danh/route number, bất kể màu nền | **IGNORE (Không vẽ box)** | — | Nằm ngoài 43 class GTSDB; gồm cả cụm nhiều panel trên cùng cột như `GTS21` |
| Biển bãi đỗ xe (chữ P xanh), biển một chiều (mũi tên trắng) | **IGNORE (Không vẽ box)** | — | Nằm ngoài 43 class GTSDB |
| Biển quay lưng (mặt sau kim loại) | **IGNORE (Không vẽ box)** | — | Không có ý nghĩa điều khiển chiều đi của ego |
| Ảnh không có bất kỳ biển nào (Negative sample) | **IGNORE (0 box)** | — | Tuyệt đối không vẽ box khống |

---

## 6. Visibility / occlusion

1. **Che khuất một phần (< 50%):** Vẽ bounding box ôm phần mặt biển hiển thị. Gán `readable = yes` nếu vẫn đọc được ký hiệu chính, gán `readable = uncertain` nếu ký hiệu bị che mất một phần quan trọng.
2. **Che khuất nặng (>= 50%):** Vẽ box phần nhìn thấy, chọn `readable = no`, `sign_class = unknown`, và bật `needs_review = true`.
3. **Cắt mép ảnh (Truncation):** Nếu biển bị cắt mép nhưng nhận ra được họ biển, vẽ box bám mép ảnh và đánh dấu `truncated = true`.

---

## 7. Ambiguity / escalation

- **Quy tắc giải quyết mơ hồ:**
  - Nếu phân vân giữa `relevant` và `not_relevant` do không rõ làn đường áp dụng: Chọn `relevance = unknown`, gán `needs_review = true`.
  - Nếu phân vân giữa 2 class tương tự (ví dụ tốc độ 30 hay 50 do mờ nét): Giữ đúng `sign_family = prohibitory`, chọn `sign_class = unknown`, đặt `readable = no`. **Tuyệt đối không đoán số.**
- **Escalation cấp ảnh (`image_escalate`):**
  - Gắn tag `image_escalate` khi: Xuất hiện biển báo mâu thuẫn trực tiếp trên cùng một làn, hoặc góc chụp khiến biển báo tạo nguy cơ tai nạn nghiêm trọng nếu suy diễn sai.

---

## 8. Temporal rule

- **Không áp dụng — task ảnh tĩnh.** Dữ liệu GTSDB gồm các ảnh đơn lẻ độc lập, không có tính liên tục theo thời gian giữa các sample.

---

## 9. Examples

Dưới đây là ví dụ chuẩn từ split `example` và một ví dụ bổ sung từ blind review để người gán nhãn đối chiếu trực tiếp:

| sample_id | Thấy gì trong ảnh | Expected output (CVAT) | Rule áp dụng |
|---|---|---|---|
| `GTS05` | 1 biển giới hạn tốc độ 30 km/h cắm bên phải đường | `traffic_sign` box `[453, 411, 492, 451]`, `relevance: relevant`, `sign_family: prohibitory`, `sign_class: 01 speed limit 30`, `readable: yes` | Mục 4.1: Biển tốc độ bên phải khống chế trực tiếp xe ego |
| `GTS01` | Cột bên phải có 3 biển: đường trơn, tốc độ 50, cấm vượt; cột bên trái có 3 biển tương ứng | Vẽ 6 box riêng biệt. Cả 3 biển bên phải và 3 biển bên trái đều là `relevant` (áp dụng chung cho đường đôi cùng chiều) | Mục 2 & 4.1: Tách riêng từng biển trên cùng cột; biển cắm đối xứng 2 bên cùng có hiệu lực |
| `GTS07` | Đoạn đường trống, hai bên không có biển báo nào | Không vẽ bất kỳ box nào (0 annotation) | Mục 1 & 5: Negative sample, không sinh False Positive |
| `GTS09` | Biển `keep right` màu xanh lam cắm trên đảo tam giác phân luồng bên trái làn xe | 1 box `[392, 611, 425, 651]`, `relevance: relevant`, `sign_family: mandatory`, `sign_class: 38 keep right`, `readable: yes` | Mục 4.1: Biển trên đảo giao thông khống chế hướng đi của ego |
| `GTS21` | Có biển `27 pedestrian crossing`, biển `39 keep left` và cụm bảng chỉ hướng/địa danh nhiều panel | LABEL riêng 2 biển GTSDB (`27` và `39`); IGNORE toàn bộ cụm bảng chỉ hướng, không tạo box `unknown` cho cả cụm | Mục 1 và 5: chỉ dẫn địa danh/hướng đi ngoài danh mục 43 class, bất kể màu nền |

---

## 10. Common mistakes

1. **Vẽ gộp cụm biển trên cùng cột vào 1 box lớn:** Sai nghiêm trọng. Mỗi biển báo là một vật thể độc lập và có mức độ liên quan khác nhau.
2. **Vẽ box vào biển phụ (Zusatzzeichen), biển bãi đỗ xe P, biển một chiều, hoặc biển tên thành phố:** Đây là lỗi vẽ thừa (False Positive). Các biển này nằm ngoài 43 class GTSDB, bắt buộc phải IGNORE.
3. **Nhầm lẫn giữa IGNORE và NOT_RELEVANT:** 
   - Biển nằm ngoài 43 class $\rightarrow$ IGNORE (không vẽ box).
   - Biển thuộc 43 class nhưng chỉ cấm xe tải (`10, 16`) hoặc ở nhánh rẽ $\rightarrow$ VẪN VẼ BOX, nhưng gán `relevance = not_relevant`.
4. **Gán `relevant` cho biển cấm xe tải (`10 no overtaking (trucks)`):** Lỗi Critical. Xe ego là xe con, không bị khống chế bởi biển cấm dành riêng cho xe tải.
5. **Kéo box trùm qua chân cột đỡ:** Gây méo mó hình học và sai lệch IoU khi đánh giá mô hình object detection.
6. **Đoán class khi biển bị mờ nhòe:** Khi không đọc được số tốc độ, phải chọn `sign_class = unknown` thay vì tự đoán một con số ngẫu nhiên.
7. **Quên chọn thuộc tính để sót `__undefined__`:** Phải kiểm tra lại toàn bộ danh sách object trước khi export.
8. **Gán family chỉ theo hình tam giác:** `13 give way` và `11 priority at next intersection` đều thuộc `other`; không chuyển sang `danger` chỉ vì có viền đỏ hình tam giác.
9. **Vẽ cụm bảng chỉ đường như một biển `unknown`:** IGNORE toàn bộ bảng chỉ hướng/địa danh/route number ngoài taxonomy, kể cả khi nhiều panel cùng cột (`GTS21`).
10. **Để nguyên `readable=uncertain` theo default:** mở từng object và chọn giá trị đúng theo độ rõ của biểu tượng; default CVAT không thay cho đánh giá.
