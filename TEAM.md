# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `BanCuoiE402`
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-BanCuoiE402-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): *(chưa tới phút 125 — sẽ điền ở Vòng 2)*

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Đàm Hồng Thái | 2A202603927 | Kỹ sư cổng | |
|   2 | Nguyễn Hữu Mạnh | 2A202604015 | Kỹ sư cổng | |
|   3 | Phan Nguyễn Phan Anh | 2A202604004 | Sản phẩm và kinh doanh | |
|   4 | Lê Quý Toàn | 2A202603941 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## LeQuyToan-2A202603941

### Phần việc phụ trách

Vai **Vận hành và pháp lý** (kiêm thư ký tổng hợp nộp bài):
- `templates/form-a-criteria.md`: mục A1 (câu 1.2) và mục A2 (câu 1.4 — telemetry production).
- `templates/form-b-evaluation-gates.md`: mục B4 (HAZOP vòng 1), B5 (Checklist 9 nhóm lần 1 — vận hành & pháp lý), B7.5 (Runbook 1–3) và B7.6 (Giờ cao điểm).
- `config/operating_gates.json`: điền khối `operations` và `legal` (giữ nguyên khối `business` cho vai Sản phẩm và kinh doanh).
- Theo lịch làm việc nhóm: rà soát `submission/` và `lab10.check_submission` ở cuối buổi (khi có đủ bài của 3 thành viên còn lại).

### Đóng góp cụ thể

- Hoàn thành phần Vận hành & Pháp lý và tổng hợp hoàn thiện **Phần A (CP1 + CP2 + CP3)**:
  - Tổng hợp bản `config/acceptance_criteria.json` và `templates/form-a-criteria.md` từ nhánh `2A202604004`, chuẩn hoá LF qua `.gitattributes`, điền `team` (`K5-L3B-DAY10-BanCuoiE402-PoCtoPilotGate1`) + `signed_by` (`Phan Anh`), chạy `lab10.criteria sign` (`fbb38de`, `2026-11-19T15:26:28`) trước mọi lần chạy `eval`.
  - Hoàn thiện `config/operating_gates.json` (đủ `business`, `operations`, `legal`), code 3 cổng phòng ngừa vòng 1 trong `lab10/guards.py` (`pre_guard`, `_check_issue_refund`, `_check_carrier_fault`), hoàn thiện toàn bộ `Phiếu B` (`B0`–`B8`, Runbook 1–3, Giờ cao điểm, kiểm thử hành vi `--adhoc`), chạy `lab10.checkpoint` (`99b636e9`) và chốt quyết định `v1`.

### Bằng chứng

- Commit ký tiêu chí: `024b11e` (hash `a8a62335...`, `2026-11-19T15:43:37`)
- Chốt cổng vòng 1 (`checkpoint`): `da2f415e` (`lab10/guards_round1.py`, `config/operating_gates.round1.json`, `config/round1.lock`)
- Các lần chạy Vòng 1: `R-base-before-20261119-154446-db8f18` (base), `R-base-after-20261119-154448-db8f18` (after), `R-base-prepared-20261119-154450-db8f18` (prepared)
- Phiếu đã điền: `templates/form-a-criteria.md` (`A1–A5`), `templates/form-b-evaluation-gates.md` (`B0–B8`)

### Khai báo sử dụng AI

- Có sử dụng trợ lý AI hỗ trợ rà soát đề bài, kiểm tra nhất quán cấu hình/trace, đối chiếu công thức và soạn thảo nháp; toàn bộ số liệu, lệnh chạy và kết quả kiểm thử đều do thành viên trực tiếp chạy kiểm chứng trong repo.

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
