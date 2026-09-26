# Annotation guideline — Xác định Biển báo Giao thông & Mức độ Liên quan tới Xe Tự hành (Ego-Relevance)

**Version:** v2

Tài liệu này là quy chuẩn hướng dẫn gán nhãn cho dự án Nhận diện & Đánh giá Hiệu lực Biển báo Giao thông đối với xe tự hành (Ego Vehicle) trên bộ dữ liệu GTSDB. Người gán nhãn phải tuân thủ nghiêm ngặt các quy tắc dưới đây mà không dựa vào phỏng đoán cá nhân.

---

## 1. Objective + scope

- **Mục tiêu:** Cung cấp dữ liệu huấn luyện cho hệ thống lái xe tự hành L2+/L3 (Module ADAS Motion Planning & Speed Advisory). Xe tự hành mục tiêu là **xe con chở khách tiêu chuẩn (standard passenger car)**. Mô hình cần biết:
  1. Vị trí chính xác của từng biển báo phía trước.
  2. Loại biển báo (cấm, hiệu lệnh, nguy hiểm, cảnh báo).
  3. **Biển báo đó có bắt buộc xe ego phải tuân thủ hành vi hay không (`relevance`)**.
- **Phạm vi trong scope (bắt buộc gán nhãn):**
  - Mọi biển báo giao thông chuẩn thuộc 4 nhóm (prohibitory, mandatory, danger, other) hướng mặt về phía xe (nhìn thấy được mặt trước hoặc biểu tượng) có kích thước $\ge 10\times 10$ pixels.
  - Bao gồm biển cắm bên phải đường, bên trái đường, trên dải phân cách giữa/đảo giao thông, và trên giá long môn.
- **Phạm vi ngoài scope (bỏ qua - IGNORE, không vẽ box):**
  - Mặt sau của biển báo quay về hướng xe ego (chỉ thấy lưng kim loại hoặc khung đỡ).
  - Biển báo bị che khuất hoàn toàn ($100\%$).
  - Biển quảng cáo, biển tên đường nhỏ, biển số nhà, biển báo công trình tư nhân không thuộc hệ thống biển báo đường bộ chuẩn.
  - Biển quá nhỏ ($< 10\times 10$ pixels) hoặc mờ nhòe tới mức mắt người không thể nhận diện được hình dạng hình học.

---

## 2. Annotation unit

- **Đơn vị gán nhãn:** Ảnh tĩnh độc lập (Single-frame Image).
- **Loại hình học:** Hình chữ nhật độc lập (Instance Bounding Box - 2D Rectangle).
- Mỗi biển báo vật lý là một instance riêng biệt. Nếu trên cùng một cột có nhiều biển báo treo chồng lên nhau, **mỗi biển báo phải được vẽ một bounding box riêng**, không vẽ gộp cả cụm biển vào một box lớn.

---

## 3. Geometry rule

- **Tight bounding box:** Bounding box phải ôm khít viền mép ngoài cùng của mặt biển hiển thị (visible boundary).
- **Không bao gồm phụ kiện:** Tuyệt đối không kéo box trùm qua cột đỡ, thanh giằng kim loại, giá treo hoặc khoảng trống nền trời xung quanh.
- **Biển bị che một phần (Occlusion):** Vẽ box ôm trọn phần nhìn thấy được của mặt biển (visible area). Nếu phần bị che $\ge 10\%$ diện tích biển nhưng vẫn nhận biết được hình học, bật cờ `needs_review`.
- **Dung sai hình học (Tolerance):** Sai số biên $\le 3$ pixels ở mỗi cạnh so với mép thực tế của mặt biển.

---

## 4. Taxonomy & Attributes

Mỗi bounding box `traffic_sign` phải được gán đủ các thuộc tính sau (không được để sót `__undefined__`):

### 4.1 Thuộc tính `relevance` (Hiệu lực đối với xe Ego)
Đây là thuộc tính quan trọng nhất cho downstream model:
- **`relevant` (Có hiệu lực / Bắt buộc tuân thủ):**
  1. Biển đặt bên phải đường cùng chiều, khống chế trực tiếp làn xe ego đang di chuyển (ví dụ: biển giới hạn tốc độ, biển báo nguy hiểm đường cong, công trường, động vật qua đường).
  2. Biển cắm trên đảo giao thông hoặc dải phân cách trực tiếp phía trước hướng đi của xe (ví dụ: `38 keep right`, `39 keep left`, `40 roundabout`).
  3. Cặp biển cắm đối xứng hai bên đường (cả bên trái và bên phải, như trên cao tốc hoặc đường một chiều) có hiệu lực chung cho toàn bộ các làn xe cùng chiều (ví dụ: cặp biển `08 speed limit 120` ở cả hai bên đường trong `GTS04`, `GTS08`).
  4. Biển `14 stop` hoặc `13 give way` tại giao lộ phía trước mà xe ego chuẩn bị tiến vào.
- **`not_relevant` (Không áp dụng cho Ego):**
  1. **Biển áp dụng cho phương tiện khác:** Điển hình là các biển chỉ dành riêng cho xe tải như `10 no overtaking (trucks)`, `16 no trucks`, hoặc biển hết hạn chế xe tải `42 restriction ends (overtaking (trucks))`. Vì xe ego là xe con standard, các biển này không khống chế quyền đi hay vượt của ego.
  2. **Biển dành riêng cho làn rẽ hoặc đường nhánh:** Biển cắm trên nhánh đường phụ/đường gom rẽ nhánh mà xe ego không đi vào (khi ego đang chạy trên trục đường chính).
  3. **Biển hướng sang hướng đường cắt ngang:** Biển báo cắm phục vụ cho phương tiện ở luồng đường giao cắt mà không áp dụng cho chiều đi của ego.
- **`unknown` (Chưa đủ bằng chứng xác định):**
  - Biển ở quá xa hoặc bị che khuất khiến không thể xác định biển điều khiển làn nào, hoặc giao lộ quá phức tạp.

### 4.2 Thuộc tính `sign_family` (Họ biển báo)
- `prohibitory`: Biển báo cấm (hình tròn viền đỏ nền trắng, hoặc viền đỏ có gạch chéo, hoặc biển cấm đi vào).
- `mandatory`: Biển hiệu lệnh bắt buộc (hình tròn nền xanh lam có mũi tên trắng).
- `danger`: Biển cảnh báo nguy hiểm (hình tam giác đều đỉnh hướng lên, viền đỏ nền trắng/vàng).
- `other`: Biển ưu tiên (hình thoi vàng `priority road`, tam giác ngược `give way`, bát giác `stop`), biển hết hạn chế (`restriction ends`), biển chỉ dẫn vuông/chữ nhật.
- `unknown`: Không thể nhận diện được hình dạng/màu sắc họ biển.

### 4.3 Thuộc tính `sign_class` (Mã biển chi tiết GTSDB)
Chọn 1 trong 43 mã biển chuẩn từ `00` đến `42` theo danh mục GTSDB. Nếu biểu tượng bên trong bị mờ, lóa hoặc quá xa không đọc được số/icon, chọn `unknown`.

### 4.4 Thuộc tính chất lượng
- `readable`:
  - `yes`: Đọc rõ ràng con số/biểu tượng mặt biển ở tỷ lệ thu phóng $100\%$.
  - `no`: Nhìn thấy có mặt biển nhưng không thể đọc được nội dung bên trong.
  - `uncertain`: Nửa rõ nửa mờ, phán đoán không chắc chắn.
- `truncated`: Checkbox `true` nếu biển bị mép ảnh cắt mất một phần.
- `needs_review`: Checkbox `true` nếu là ca biên cần xem xét lại.

---

## 5. Inclusion / exclusion

| Trường hợp | Hành động | Giải thích |
|---|---|---|
| Biển trên cùng cột cắm bên phải đường | LABEL từng biển riêng | Mỗi biển một box, gán relevance độc lập |
| Biển `10 no overtaking (trucks)` cắm cùng cột với biển tốc độ | LABEL cả hai | Biển tốc độ: `relevant`; biển cấm xe tải vượt: `not_relevant` |
| Biển quay lưng (mặt sau) | IGNORE | Không có ý nghĩa điều khiển chiều đi của ego |
| Biển cắm ở đảo phân làn bên trái (`keep right`) | LABEL (`relevant`) | Hướng dẫn xe ego phải đi vòng qua bên phải đảo |
| Ảnh không có bất kỳ biển nào (Negative sample) | IGNORE (0 box) | Tuyệt đối không vẽ box khống |

---

## 6. Visibility / occlusion

1. **Che khuất một phần ($< 50\%$):** Vẽ bounding box ôm phần mặt biển hiển thị. Gán `readable = yes` nếu vẫn đọc được ký hiệu chính, gán `readable = uncertain` nếu ký hiệu bị che mất một phần quan trọng.
2. **Che khuất nặng ($\ge 50\%$):** Vẽ box phần nhìn thấy, chọn `readable = no`, `sign_class = unknown`, và bật `needs_review = true`.
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

Dưới đây là 4 ví dụ chuẩn từ split `example` để người gán nhãn đối chiếu trực tiếp:

| sample_id | Thấy gì trong ảnh | Expected output (CVAT) | Rule áp dụng |
|---|---|---|---|
| `GTS05` | 1 biển giới hạn tốc độ 30 km/h cắm bên phải đường | `traffic_sign` box `[453, 411, 492, 451]`, `relevance: relevant`, `sign_family: prohibitory`, `sign_class: 01 speed limit 30`, `readable: yes` | Mục 4.1: Biển tốc độ bên phải khống chế trực tiếp xe ego |
| `GTS01` | Cột bên phải có 3 biển: đường trơn, tốc độ 50, cấm vượt; cột bên trái có 3 biển tương ứng | Vẽ 6 box riêng biệt. Cả 3 biển bên phải và 3 biển bên trái đều là `relevant` (áp dụng chung cho đường đôi cùng chiều) | Mục 2 & 4.1: Tách riêng từng biển trên cùng cột; biển cắm đối xứng 2 bên cùng có hiệu lực |
| `GTS07` | Đoạn đường trống, hai bên không có biển báo nào | Không vẽ bất kỳ box nào (0 annotation) | Mục 1 & 5: Negative sample, không sinh False Positive |
| `GTS09` | Biển `keep right` màu xanh lam cắm trên đảo tam giác phân luồng bên trái làn xe | 1 box `[392, 611, 425, 651]`, `relevance: relevant`, `sign_family: mandatory`, `sign_class: 38 keep right`, `readable: yes` | Mục 4.1: Biển trên đảo giao thông khống chế hướng đi của ego |

---

## 10. Common mistakes

1. **Vẽ gộp cụm biển trên cùng cột vào 1 box lớn:** Sai nghiêm trọng. Mỗi biển báo là một vật thể độc lập và có mức độ liên quan khác nhau.
2. **Gán `relevant` cho biển cấm xe tải (`10 no overtaking (trucks)`):** Đây là lỗi Critical. Xe ego là xe con, không bị khống chế bởi biển cấm dành riêng cho xe tải.
3. **Kéo box trùm qua chân cột đỡ:** Gây méo mó hình học và sai lệch IoU khi đánh giá mô hình object detection.
4. **Đoán class khi biển bị mờ nhòe:** Khi không đọc được số tốc độ, phải chọn `sign_class = unknown` thay vì tự đoán một con số ngẫu nhiên.
5. **Quên chọn thuộc tính để sót `__undefined__`:** Phải kiểm tra lại toàn bộ danh sách object trước khi export.
