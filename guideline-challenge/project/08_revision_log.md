# Revision log

Guideline v1 = bản nháp đầu; v2 = sau calibration nội bộ; v3 = sau blind handoff. Mỗi lần tăng `Version` trong
`02_guideline.md`, thêm một hoặc nhiều dòng vào bảng: đổi gì và vì sao, kèm bằng chứng (sample_id, dòng
calibration report, câu hỏi trong clarification log, feedback của peer).

Cột Version ghi dạng `v1`, `v2`, `v3` — `make status` tìm dòng bảng có `v2` và dòng có `v3`.

| Version | Đổi gì | Vì sao | Bằng chứng |
|---|---|---|---|
| v1 | Khởi tạo Guideline v1 với 10 mục bắt buộc | Định hình phạm vi và bộ quy tắc gán nhãn ban đầu | `01_problem_statement.md`, `03_cvat_labels.json` |
| v2 | Bổ sung quy tắc xe con cho biển xe tải (`not_relevant`), cấm đoán số khi `readable=no`, và làm rõ biển đảo giao thông | Kết quả bất đồng calibration nội bộ cho thấy annotator nhầm lẫn biển xe tải và phỏng đoán class khi biển ở xa | `06_calibration_report.csv` dòng GTS04, GTS03, GTS06 |
| v2 | Xóa 'biển chỉ dẫn vuông/chữ nhật' khỏi nhóm other; liệt kê cụ thể vào danh sách IGNORE: biển địa danh/khoảng cách, biển P, biển một chiều, biển phụ; phân biệt rạch ròi giữa IGNORE và NOT_RELEVANT | Loại bỏ hoàn toàn nguy cơ annotator vẽ box thừa (False Positive) vào các biển nằm ngoài 43 class GTSDB | Thảo luận calibration thực tế trên `GTS03` và phản hồi trực tiếp từ người gán nhãn |
| v3 | Nêu rõ biển chỉ hướng/địa danh/route number mọi màu nền phải IGNORE; làm nổi bật class 13 give way và class 11 priority at next intersection thuộc `other`; yêu cầu chọn `readable` chủ động thay vì để default; thêm ví dụ GTS21 | Blind feedback cho thấy scope bảng nhiều panel chưa đủ cụ thể, default `uncertain` dễ bị bỏ nguyên, và peer phân family theo hình tam giác. Blind review cũng phát hiện expected/sample description sai ảnh ở các mẫu; gold giữ nguyên vì đã freeze | `peer_feedback.md` feedback 2–5; `Mixigaming-blind.zip`; 11 dòng `gold sai:` và ghi chú peer riêng trong `transfer_score.csv` |

