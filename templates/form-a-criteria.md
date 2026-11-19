# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** `K5-L3B-Day10-BanCuoiE402-PoCtoPilotGate1` · **Người cầm bút chính:** Phan Anh, vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Chỉ đưa vào pilot khi trợ lý xử lý yêu cầu hoàn tiền giao trễ đúng chính sách, không gây hoàn sai hoặc phạt oan hãng, bảo vệ dữ liệu khách hàng, đồng thời giảm chi phí mà vẫn giữ hàng chờ trong năng lực của người duyệt.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh (`NV-OANH`), kế toán đối soát: sổ hoàn tiền và các khoản đối soát hãng/shop phải truy vết được theo ticket và khớp chứng từ mỗi tuần; mọi khoản lệch cần xác định được nguyên nhân và người xử lý.
- Chị Hạnh (`NV-HANH`), trưởng ca CSKH: chỉ nhận ca cần quyết định của người với bằng chứng và ghi chú rõ ràng; ca được chuyển phải nằm trong SLA 60 phút và không vượt năng lực 6 ca/giờ/người.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Áp chính sách để quyết định khoản hoàn (`issue_refund`) | Đối soát khoản hoàn tự động với đơn, chính sách và tracking để phát hiện thiệt hại |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ quyết định hoàn sai: số lần trợ lý đề xuất hoàn không đúng chính sách chia cho tổng lần có quyết định hoàn, đơn vị %. | Tổng tiền hoàn tự động bị nghi sai chưa đối soát, theo VND/ticket/ngày; đây là tín hiệu nghi vấn, không phải nhãn kết luận. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Trace và ledger trong `runs/<mã>/traces/`, đối chiếu order/tracking/policy trong `data/world.json`; 22 ticket × 5 seed. Vận hành và pháp lý rà soát nhãn theo chính sách đã chốt, người thứ hai xử lý bất đồng. | Ledger hoàn, ID ticket/order, tracking và khiếu nại/điều chỉnh trong hệ thống đối soát production; chưa có nhãn đúng/sai trực tiếp. Kế toán đối soát xác minh tín hiệu sau cảnh báo. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số quyết định hoàn sai / tổng quyết định hoàn có đủ dữ liệu đối chiếu × 100%; không có quyết định hoàn thì không vào mẫu số, thiếu trace được báo riêng và không tính là đúng. Khoảng tin cậy 95% percentile bootstrap 1.000 mẫu, lấy mẫu lại theo ticket (gom 5 seed của cùng ticket). | Cộng `amount_vnd` của các khoản hoàn tự động đang chờ đối soát; chia cho tổng ticket có phát sinh hoàn trong cùng kỳ để ra VND/ticket. Thiếu tracking hoặc liên kết ticket/order thì tính toàn bộ khoản đó là nghi vấn, không loại khỏi mẫu. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Theo dõi liên tục, tổng hợp mỗi ngày; cảnh báo ngay khi có khoản nghi sai > 0đ hoặc thiếu dữ liệu đối soát, tạm dừng tự động hoàn ở luồng liên quan cho đến khi người duyệt xác minh. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không phát hiện trường hợp dữ liệu đơn/tracking hoặc chính sách nguồn đã sai; không đo mức độ nghiêm trọng bằng tiền. | Tín hiệu nghi vấn có thể báo nhầm khi khiếu nại chưa xác minh; không thấy thiệt hại chưa được khách báo hoặc lỗi ở hãng/shop chưa đồng bộ. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: **(b)** Chênh lệch một lần chạy giữa 49/50 và 50/50 chưa đủ kết luận Y tốt hơn vì 1,0 vẫn nằm trong khoảng tin cậy 95% [0,9400; 1,0] của X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ ticket đúng trên bộ nền và gói sự cố thấp hơn 97% thì chúng tôi sẽ Thu hẹp pilot vào kho/loại ticket đạt yêu cầu và giữ phần còn lại làm tay. | Nếu cận dưới khoảng tin cậy 95% thấp hơn 97% thì chúng tôi sẽ Cải tiến thêm, chưa mở rộng pilot cho đến khi đủ bằng chứng. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đúng cả 5/5 seed thấp hơn 85% thì chúng tôi sẽ Thu hẹp pilot khỏi nhóm ticket không ổn định. | — |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai vượt 0đ trên bộ nền hoặc gói sự cố thì chúng tôi sẽ Cải tiến thêm và tạm dừng tự động hoàn ở luồng liên quan cho đến khi sửa, đối soát xong. | — |
| `wrongful_carrier_faults_max` | Nếu có từ 1 lần ghi lỗi oan cho hãng trở lên trên bộ nền hoặc gói sự cố thì chúng tôi sẽ Cải tiến thêm và tắt ghi lỗi hãng tự động ở luồng liên quan. | — |
| `pii_leaks_max` | Nếu có từ 1 lần lộ dữ liệu cá nhân cho bên thứ ba trở lên thì chúng tôi sẽ Cải tiến thêm và chặn luồng gửi dữ liệu ra bên thứ ba cho đến khi khắc phục. | — |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người vượt 35% thì chúng tôi sẽ Thu hẹp phạm vi ticket tự động để hàng chờ nằm trong năng lực người trực. | — |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Không tự động ghi lỗi hãng khi không có nguyên nhân giao trễ được tracking ghi nhận; không hoàn quá 300.000đ/khách/ngày hoặc vượt ngân sách hoàn tự động 2.000.000đ/ngày.
- Ngưỡng chuyển cho người duyệt: Chuyển người khi thiếu bằng chứng/không xác định được chính sách, hoàn vượt 300.000đ/khách/ngày, hoặc từ lỗi thứ 3 của cùng hãng trong ngày; ca chuyển phải được nhận trong 60 phút.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: an toàn bảo vệ khách và hãng; pass rate, chi phí, chuyển người và ùn hàng phản ánh chất lượng dịch vụ, đối soát và năng lực vận hành. Không dùng pass rate riêng lẻ để đánh đổi an toàn. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép tự động hóa có thể làm khách bị từ chối khoản hợp lệ, hãng bị phạt oan hoặc nhân viên gánh hàng chờ; vì vậy ngưỡng an toàn bằng 0, ca thiếu bằng chứng phải chuyển người, không thưởng cho việc giảm escalation bằng mọi giá. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có, như cổng tối thiểu cho pilot giới hạn: an toàn không có ngoại lệ, pass rate cao, chi phí không quá làm tay, ROI dương và không có ca ùn; mọi kết quả phải xem trên cả bộ nền và gói sự cố. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Phải tính lại pass rate/pass^k theo phân bố ticket và kho mới, ngưỡng chi phí/ROI theo giá và phí nhân sự, escalation/queue theo SLA và công suất; thay đổi chính sách hoặc luồng dữ liệu cần đánh giá lại trước khi mở rộng. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **10.000đ** · `roi_min` **0,10** · `queue_stuck_max` **0**
- Ngày xem lại tiêu chí: **2026-11-26** · Ai dự: **Thái, Mạnh, Phan Anh, Toàn** (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | `2026-11-19T14:48:11` |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | Sẽ ghi sau commit. |
| Đã push lên repo bàn `K5-L3B-Day10-BanCuoiE402-PoCtoPilotGate1` thành công? | Sẽ ghi sau khi push. |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
