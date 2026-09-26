# QA plan + quality gates

Kế hoạch đảm bảo chất lượng và các cổng kiểm soát chất lượng (Quality Gates) cho dự án gán nhãn Biển báo Giao thông & Hiệu lực Ego-Relevance trên GTSDB.

## Flow

Quy trình kiểm soát chất lượng tuần tự:
`Guideline v1 -> Calibration nội bộ -> Refine Guideline v2 -> Gold Freeze -> Production Labeling -> Self-QC -> Review/Peer-QC -> Rework -> Quality Gate -> Handoff v3`.

- **Ai review, review bao nhiêu:**
  - QA Owner (Nguyễn Anh Tuấn) và Spec Owner (Phan Hiếu Nghĩa) chịu trách nhiệm chính trong khâu review.
  - Review 100% các sample thuộc nhóm Blind test và Calibration. Trong sản xuất quy mô lớn, lấy mẫu ngẫu nhiên có trọng số tối thiểu 30% tổng số frame.
- **Chọn sample theo rule nào:**
  - Stratified Risk-based Sampling (Lấy mẫu phân tầng theo rủi ro): Ưu tiên 100% các ảnh có tag `critical` (chứa biển STOP, No Entry, Give Way) và `conflict` (nhiều biển trên cùng cột hoặc cắm hai bên đường), 50% ảnh `small_far` / `occlusion`, và 20% ảnh `normal`.
- **Issue được ghi ở đâu, đóng thế nào:**
  - Mọi lỗi phát hiện trong quá trình review được ghi vào `07_blind_handoff/transfer_score.csv` và `06_calibration_report.csv`.
  - Issue chỉ được đóng khi:
    1. Người gán nhãn đã sửa lại geometry/attribute trên CVAT và re-export (`action = rework`), HOẶC
    2. Guideline được bổ sung rule/example làm rõ ca biên và được ratify (`action = revise_rule` / `add_example`).
- **Khi phát hiện guideline gap thì update và version ra sao:**
  - Ghi nhận triệu chứng và bất đồng vào `08_revision_log.md`.
  - Nâng version guideline (`v1 -> v2 -> v3`). Mọi thay đổi quy tắc phải có bằng chứng từ `sample_id` và số liệu bất đồng cụ thể.

## Defect severity

Bảng phân loại mức độ nghiêm trọng của lỗi dựa trên tác động trực tiếp tới hệ thống điều khiển tự hành (Motion Planning):

| Severity | Định nghĩa cho project này | Ví dụ | Action mặc định |
|---|---|---|---|
| Critical | Lỗi làm thay đổi quyết định sống còn của xe ego: Bỏ sót hoặc đánh nhãn `not_relevant` cho biển cấm/dừng/hiệu lệnh khống chế ego; hoặc đánh nhãn `relevant` cho biển xe tải/làn khác gây phanh gấp. | Đánh nhãn `not_relevant` cho biển `14 stop` hoặc `17 no entry`; đánh nhãn `relevant` cho biển `10 no overtaking (trucks)`. | REWORK ngay lập tức; chặn release batch; đào tạo lại annotator. |
| Major | Sai lệch về phân loại họ biển/mã biển hoặc sai lệch geometry ảnh hưởng lớn đến mô hình phát hiện. | Nhầm `02 speed limit 50` thành `01 speed limit 30`; vẽ gộp 2 biển trên cùng cột vào 1 box lớn; box lệch > 5 px. | REWORK trong vòng 24h trước khi merge dữ liệu. |
| Minor | Sai lệch nhỏ về thuộc tính phụ hoặc hình học trong khoảng dung sai không làm đổi hành vi xe. | Lệch viền 2–3 px; đánh nhầm `readable = yes` trong khi biển hơi mờ (`uncertain`). | Chấp nhận (ACCEPT) hoặc sửa nhanh nếu thuận tiện. |
| Question | Tình huống mơ hồ, chất lượng ảnh quá kém hoặc xung đột luật chưa có tiền lệ trong guideline. | Biển ở cự ly quá xa không rõ hướng mũi tên; biển bị che khuất >= 70% diện tích. | Gán `relevance = unknown`, bật `needs_review`, chuyển Spec Owner xử lý. |

## Metrics

1. **Decision Accuracy (D):**
   D = (Số quyết định đúng non-geometry) / (Tổng số quyết định non-geometry)
   Đo lường độ chính xác phân loại class, họ biển và relevance.

2. **Critical Decision Correctness (C):**
   C = (Số quyết định critical đúng) / (Tổng số quyết định critical)
   Đảm bảo không xảy ra hiện tượng lọt lỗi nghiêm trọng (Critical Defect Escape).

3. **Geometry Compliance (G):**
   Tỷ lệ bounding box đạt dung sai <= 3 px ở mọi cạnh và không bao gồm cột đỡ/giá treo.

4. **Independence Score (I):**
   Đo lường tính độc lập của người nhận bàn giao (dựa trên số câu hỏi cần giải thích ngoài guideline trong `clarification_log.csv`).

## Quality gate

Các điều kiện nghiệm thu chất lượng cho từng batch dữ liệu:

```text
PASS if:
  - Critical Correctness (C) = 100% (Không chấp nhận bất kỳ critical escape nào).
  - Decision Accuracy (D) >= 85%.
  - Geometry Compliance (G) >= 90%.
  - Số lượng thuộc tính __undefined__ còn lại = 0.
REWORK if:
  - Có từ 1 lỗi Critical, HOẶC
  - Decision Accuracy (D) nằm trong khoảng 70% - 84%, HOẶC
  - Còn sót thuộc tính __undefined__ chưa chọn.
REJECT / ESCALATE if:
  - Decision Accuracy (D) < 70%, HOẶC
  - Xuất hiện xung đột hệ thống trong guideline khiến người làm liên tục hiểu sai (Guideline Gap hệ thống) -> Tạm dừng dán nhãn, triệu tập Spec Owner để cập nhật Guideline.
```

**Trade-off:** Nhóm chấp nhận dung sai hình học nhỏ (<= 3 px) và cho phép `sign_class = unknown` khi biển ở xa (`readable = no`), nhưng tuyệt đối không thỏa hiệp với lỗi `relevance` trên các biển an toàn cao (`14 stop`, `17 no entry`, `10 no overtaking (trucks)`). Sự an toàn downstream là ưu tiên số một.
