# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `BanCuoiE402`
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-BanCuoiE402-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S3` (*Hãng miền Tây bị phạt vì bão*)

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Đàm Hồng Thái | 2A202603927 | Kỹ sư cổng | |
|   2 | Nguyễn Hữu Mạnh | 2A202604015 | Kỹ sư cổng | |
|   3 | Phan Nguyễn Phan Anh | 2A202604004 | Sản phẩm và kinh doanh | |
|   4 | Lê Quý Toàn | 2A202603941 | Vận hành và pháp lý | X |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## LeQuyToan-2A202603941

### Phần việc phụ trách

**Trưởng nhóm** kiêm vai **Vận hành và pháp lý** (và tổng hợp bài nộp lên `main`):
- Chốt phân công, tổng hợp phần làm từ nhánh riêng của các bạn (`2A202604004`, `2A202603927`, `2A202604015`), sắp xếp lại thứ tự commit để `Sign acceptance criteria` và dấu thời gian ký khớp đúng quy định trước khi chạy `eval`.
- Phụ trách phần vận hành và pháp lý trong **Phiếu A** (`1.2`, `1.4`), **Phiếu B** (`B4` HAZOP vòng 1, `B5` Checklist 9 nhóm, `B7.5–B7.6` Runbook 1–3 & giờ cao điểm) và **cổng `operations`, `legal`** trong `config/operating_gates.json`.
- Phối hợp chốt Vòng 1 (`lab10.checkpoint`, quyết định `v1`); sang Vòng 2 sẽ phụ trách phần riêng của thẻ (`C3`), giả định môi trường (`C5`), Runbook phần 4–5 (`C11`) và gom `submission/` kiểm tra lần cuối.

### Đóng góp cụ thể

- **Thống nhất & ký tiêu chí (CP1–CP2):** Giữ nguyên bộ ngưỡng do Phan Anh chốt trên nhánh `2A202604004` (`pass_rate >= 0.98`, `pass_k >= 0.95`, 3 chỉ số an toàn = `0`, `cost <= 8.000đ`, `ROI >= 0.25`, `queue_stuck = 0`), điền `team` và `signed_by` vào `config/acceptance_criteria.json`. Do lúc kiểm nhánh cũ phát hiện file JSON bị lệch hash giữa CRLF trên Windows và LF trên Git, mình đã thêm `.gitattributes` khoá định dạng LF cho file này rồi chạy lại `lab10.criteria sign` trên `main` trước khi chạy `eval`.
- **Cấu hình cổng vận hành & pháp lý (`config/operating_gates.json`):** Điền đủ thông số ca trực khớp `data/world.json` (`pic: NV-TUNG`, `approver_id: NV-HANH`, `1` người trực, `6 ca/giờ`, SLA `60 phút`, bật `decision_note: true` và kiểm mẫu `10%`, kênh `#ops-logix-pilot`, `4` điều kiện dừng); bật `carrier_fault_requires_recorded_cause: true` và chặn gửi các trường nhạy cảm (`customer_note`, `recipient_contact`, `name`, `phone`, `street`) ra bên thứ ba.
- **Soạn hồ sơ & hoàn thiện Vòng 1:** Viết HAZOP cho `notify_carrier` / `file_carrier_fault` (`B4`), lập bảng Checklist 9 nhóm có PIC từng bạn (`B5`), soạn Runbook 1–3 và phương án giờ cao điểm (`B7.5–B7.6`). Sau khi chốt phương án cổng với nhóm, chạy đủ các mốc `base` → `after` → `checkpoint` → `prepared`, bổ sung phần còn thiếu ở `lab10/guards.py` và `Phiếu B` (`B0–B3`, `B6`, `B7.1–B7.4`, `B8`), ghép hàm `tracking_delay_mismatch_rate` của Mạnh vào `lab10/monitors.py`, kiểm 13/13 unit tests và đẩy lên `main`.
- **Khai báo sử dụng AI:** Mình có dùng công cụ AI để hỗ trợ đối chiếu đề bài với `data/world.json`/`lab10`, kiểm tra lỗi lệch hash/nhánh git và rà câu chữ; các lệnh chạy đo đạc, trace và test đều được chạy kiểm chứng trực tiếp trên máy trước khi commit.

### Bằng chứng

- Commit ký tiêu chí: `024b11e` (`2026-11-19T15:43:37`, hash file `a8a62335...` khớp `config/acceptance_criteria.lock`)
- Chốt cổng vòng 1 (`lab10.checkpoint`): commit `ac4dd6b`, hash `da2f415e` (`lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`)
- Cập nhật chữ ký Form A: commit `da0f743`
- Các lần chạy Vòng 1: `R-base-before-20261119-154446-db8f18` (base: `109/110`, hỏng `T-002@55`), `R-base-after-20261119-154448-db8f18` (after: `110/110`), `R-base-prepared-20261119-154450-db8f18` (prepared: `110/110`, `9/9` ngưỡng trong `lab10.gate` ĐẠT, `13/13` unit tests OK)
- Các lần chạy Vòng 2 (thẻ `S3`): `R-S3-grade-20261119-162704-db8f18` (prepared lúc mới nhận thẻ), `R-S3-after-20261119-163012-641d82` (`60/60`), `R-base-after-20261119-163126-641d82` (`110/110`), `R-S3-grade-20261119-163012-641d82` (`PASS-VISIBLE`, `5/5` kiểm tra xanh)
- File đã cập nhật: `TEAM.md`, `.gitattributes`, `config/acceptance_criteria.json`, `config/operating_gates.json`, `lab10/guards.py`, `lab10/monitors.py`, `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`, `submission/submission.json`

### Exit ticket

- **Một điều học được:** Khi viết guard phòng ngừa phải tách rõ ranh giới giữa trách nhiệm nội bộ và đối tác — ở thẻ `S3`, việc gộp nhầm điều kiện thiếu `delay_cause` vào nhánh tính hoàn tiền đã cắt nhầm `210.000đ` của khách dù chỉ cần chặn ghi lỗi hãng; tách bạch 2 nhánh và chặn thêm trần lỗi/ngày của hãng (`max_auto_strikes_per_carrier_per_day`) giải quyết gọn cả 3 nguyên nhân.
- **Một điều còn chưa chắc:** Trường hợp kho nhập **sai** nguyên nhân (gõ `"CARRIER"` cho đơn đáng lẽ là `"FORCE_MAJEURE"`) chưa thể phát hiện tự động chỉ từ dữ liệu mock hiện tại, nên cần theo dõi thực tế qua đối soát cuối ca với `NV-OANH` ở tuần pilot đầu.

---

## NguyenHuuManh-2A202604015

### Phần việc phụ trách

Kỹ sư cổng. Tham gia đối chiếu tiêu chí, dò trace, thêm chỉ số theo dõi `tracking_delay_mismatch_rate` trong `lab10/monitors.py` (ghép từ nhánh `2A202604015`).

### Đóng góp cụ thể

- Thêm `tracking_delay_mismatch_rate` vào `lab10/monitors.py` (`MONITORS`) để đếm tỉ lệ lượt model dùng số ngày trễ khác tracking (`0.009091` = `1/110` lượt trên bộ nền).
- Khai báo sử dụng AI: Có sử dụng Codex để đọc code, viết chỉ số và đối chiếu bằng chứng chạy lab.

### Exit ticket

- *(Sẽ cập nhật sau khi cả nhóm hoàn tất Vòng 2 và chạy `lab10.grade`)*

---

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
