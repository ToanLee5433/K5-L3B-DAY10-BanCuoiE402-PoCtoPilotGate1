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

Kỹ sư cổng. Đối chiếu tiêu chí đã ký, chạy đánh giá và dò trace trên bộ nền và thẻ S3. Viết và kiểm chứng các chỉ số theo dõi ở Phiếu C mục C8.

### Đóng góp cụ thể

- Đăng ký `tracking_delay_mismatch_rate` để đo tỉ lệ lượt model dùng số ngày trễ khác tracking. Bổ sung `policy_index_mismatch_rate` và `carrier_strike_cap_hit_rate` để theo dõi hai nguyên nhân khác của S3.
- Chạy lại S3 và hồi quy bộ nền trên bản mới của nhóm. Khôi phục đúng định dạng xuống dòng của bản chốt để lệnh `lab10.checkpoint verify` kiểm được hash trên checkout mới.
- Có dùng Codex để đọc code, viết chỉ số và đối chiếu bằng chứng chạy lab.

### Bằng chứng

- Bộ nền `R-base-after-20261119-164821-d1e2fa` đạt 110/110 lượt. Trace `T-002@55` qua cổng và chỉ số lệch độ trễ ghi nhận 1/110 lượt.
- S3 `R-S3-grade-20261119-164821-d1e2fa` đạt `PASS-VISIBLE`, mốc after đạt 60/60 lượt. Trace `S3-01@11` ghi index v3 lệch phiên bản hiệu lực v4 và `S3-42@11` ghi cổng chặn khi MKD đã có hai lỗi trong ngày. [Báo cáo ba mốc](submission/runs/grade-report.md).
- 13/13 bài kiểm thử công khai đạt.

### Exit ticket

Một ca có thể được hoàn đúng phí trong khi lệnh ghi lỗi cho hãng phải dừng. Cần đối soát sau bão để biết nguyên nhân trễ cập nhật muộn đến mức nào và kiểm chứng tỉ lệ cảnh báo trong ca thật.

---

## DamHongThai-2A202603927

### Phần việc phụ trách

Kỹ sư cổng. Phụ trách phần kỹ thuật trong vòng 1: Câu 2.1–2.2 (chạy đánh giá, dò `T-002@55`), Câu 2.6–2.8 (`lab10/guards.py`, bảo vệ lệnh ghi, kiểm behavioral test). Tiếp tục vai kỹ sư cổng ở vòng 2: Câu 3.1–3.5, trace thẻ `S3`, sửa guard và kiểm chứng ba mốc `base → prepared → after`.

### Đóng góp cụ thể

- Tham gia đối chiếu baseline và phân tích lỗi chìm `T-002@55`: phát hiện model dùng `delay_days = 5` từ lời khách thay vì `db_delay_days = 2`, dẫn tới hoàn sai `20.000đ` và ghi/lây lỗi oan cho hãng `VNX`.
- Tham gia thiết kế và kiểm chứng các cổng viết trước lệnh ghi trong `lab10/guards.py`: đối chiếu quyền lợi qua tracking/policy, chặn hoàn sai hoặc hoàn lặp, chặn ghi/lọc trường hãng, và chuyển ca thiếu căn cứ sang người duyệt.
- Tham gia behavioral test, unit test và các lần chạy `base`/`S3`; xác nhận sau sửa không hoàn sai, không ghi lỗi hãng oan, không lộ PII và không có regression so với bộ nền.
- Là PIC chất lượng và quyền hạn trong Phiếu B mục B5, đồng thời là PIC của nhóm chất lượng khi cập nhật checklist sau thẻ `S3` ở Phiếu C mục C11.

### Bằng chứng

- Dấu vết nhánh kỹ thuật `origin/2A202603927`: commit `500c337` bổ sung cổng vòng 1 và `guard_intervention_rate`; hồ sơ nộp dùng tiêu chí và bản chốt chung trên `main`.
- Bộ nền vòng 1: `R-base-before-20261119-154446-db8f18` phát hiện hoàn sai `20.000đ`, `1` lỗi hãng oan; `R-base-after-20261119-154448-db8f18` đạt `110/110`, hoàn sai `0`, lỗi hãng oan `0`, PII `0`; `R-base-prepared-20261119-154450-db8f18` giữ `100%` và `13/13` unit tests.
- Thẻ `S3`: `R-S3-after-20261119-163012-641d82` đạt `60/60`; `R-base-after-20261119-163126-641d82` đạt `110/110` không regression; `lab10.grade --incident S3` đạt `PASS-VISIBLE`.
- File chính: `lab10/guards.py`, `lab10/monitors.py`, `config/operating_gates.json`, `Phiếu B B2/B5/B7.1–B7.3`, `Phiếu C C2/C7/C11`.

### Exit ticket

- **Một điều học được:** Cổng an toàn phải đối chiếu lệnh ghi với tracking, chính sách và sổ lịch sử thay vì tin dữ liệu do model hoặc khách khai; dữ liệu bị thiếu cũng cần chặn hoặc chuyển duyệt thay vì fail-open.
- **Một điều còn chưa chắc:** Cần theo dõi dữ liệu production để phân biệt tracking bị trễ cập nhật với tracking thực sự sai, tránh vừa chặn tác hại vừa tạo quá nhiều ca chuyển người cho kiện hợp lệ.

---

## PhanNguyenPhanAnh-2A202604004

### Phần việc phụ trách

Vai **Sản phẩm và kinh doanh**. Chủ trì Phiếu A câu 1.1, 1.5, 1.6; tổng hợp đầu vào cách đo từ các vai liên quan. Phụ trách Phiếu B B3, lăng kính kinh doanh ở B6, B7.4 và nội dung quyết định v1 tại B8; sang S3 đối chiếu C3.5, specification ở C5, rủi ro chính sách/chi phí tại C10, quyết định v2 và ba dòng bắt buộc tại C12. Phối hợp hoàn thiện cấu hình business, điều kiện dừng kinh tế và `submission/submission.json`.

### Đóng góp cụ thể

- Hoàn thiện mục tiêu cấp hệ thống và tiêu chí trước khi đo: pass_rate >= 98%, pass^k >= 95%, ba chỉ số an toàn = 0, chi phí <= 8.000đ/ticket, ROI >= 0,25 và 0 ca ùn. Giải thích mức 8.000đ là tiết kiệm 20% so với làm tay 10.000đ và tương ứng ROI tối thiểu 25%; giữ nguyên tiêu chí sau ký.
- Phân tích nguồn sự thật/bản sao và drift REFUND-v4 từ 01/12/2026, tác động tới quyền hoàn, hạn mức duyệt và lỗi hãng. Đối chiếu cổng business theo ngân sách 2.000.000đ/ngày, tiền máy 1.500đ/ticket và phạm vi pilot đã thử.
- Tổng hợp căn cứ v1/v2: nền sau cổng đạt 110/110; S3 đi từ 900.000đ hoàn sai và 35 lỗi hãng oan về 0 ở after, chi phí 4.405đ/ticket và ROI 1,27. Đọc thêm hoàn thiếu và chi phí nhóm thiếu mã đơn để không bỏ sót quyền lợi khách/phân khúc khó.
- Kiểm chứng phương án 1–2 người duyệt bằng bản sao config trong bộ nhớ: S3 tăng từ 4.405đ lên 6.905đ/ticket khi bố trí thêm người thường trực. Thử riêng kịch bản 18 ca cần duyệt/giờ cho thấy 2 người giảm chờ tối đa từ 113,3 xuống 28,3 phút; dùng làm phương án dự phòng, không gán thành lưu lượng production.
- Đồng bộ điều kiện dừng vận hành v2 với bản tiêu chí đã ký; cập nhật C11/C12 và ba dòng bắt buộc, hoàn thiện mục cá nhân trong TEAM.md và gom hồ sơ nộp trên kết quả kiểm tra cuối. Phần guard/monitor kỹ thuật là đóng góp phối hợp của nhóm, không tính là phần tôi tự triển khai.

### Bằng chứng

- Commit nội dung CP2 `1f4e5c6`; commit ký `024b11e`, hash tiêu chí `a8a62335`; chốt vòng 1 `ac4dd6b`, hash `da2f415e`.
- V1: `R-base-prepared-20261119-154450-db8f18`; v2 kiểm tra cuối: `R-S3-grade-20261119-171423-7fc336` và `R-base-after-20261119-171423-7fc336`.
- Report cuối ghi `PASS-VISIBLE`, 13/13 test công khai đạt; integrity, criteria, visible, regression, monitor đều đạt; test ẩn chưa có trên máy.
- [Bằng chứng kinh doanh](submission/runs/business-analysis-2A202604004.json); [báo cáo ba mốc](submission/runs/grade-report.md).

### Exit ticket

- **Điều học được:** giảm phí xử lý không thể bù cho hoàn sai hoặc phạt oan hãng; chi phí cần tính cả công duyệt, kiểm mẫu và phí trực. Phải tách quyền hoàn của khách khỏi quyền ghi lỗi hãng khi thiếu nguyên nhân.
- **Điều còn chưa chắc:** độ trễ cập nhật nguyên nhân sau bão, tỷ lệ nhập sai và công đối soát thực tế chưa có trong dữ liệu mock; cần đo trong 7 ngày đầu pilot trước khi mở rộng.
