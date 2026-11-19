"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không tìm thấy chính sách hoàn tiền đang có hiệu lực")
    ctx.log("policy_pinned", policy_id=policy["policy_id"])
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    tool = action.get("tool")
    policies = ctx.tools.lookup_policies()
    policy = H.effective_policy(policies, ctx.as_of)

    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order is None or order.get("customer_id") != ctx.ticket.get("customer_id"):
            return Verdict.escalate("không xác minh được đơn và chủ đơn từ nguồn dữ liệu")
        if policy is None:
            return Verdict.escalate("không tìm thấy chính sách hoàn tiền đang có hiệu lực")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        cause = parcel.get("delay_cause")
        if cause is None:
            return Verdict.escalate("tracking chưa ghi nguyên nhân trễ; cần người xác minh")
        delay = H.db_delay_days(parcel, ctx.as_of)
        entitlement = H.entitlement_vnd(policy, order, delay, cause)
        if action.get("payer") != "LOGIX":
            return Verdict.escalate("bên chịu tiền hoàn không được xác minh; cần người duyệt")
        if action.get("amount_vnd", 0) > entitlement:
            return Verdict.escalate("số tiền đề xuất vượt quyền lợi tính từ tracking và chính sách hiệu lực")

    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order is None or policy is None:
            return Verdict.deny("không xác minh được đơn hoặc chính sách hiệu lực")
        parcel = next((p for p in order["parcels"] if p.get("parcel_id") == action.get("parcel_id")), None)
        if parcel is None:
            return Verdict.deny("kiện hàng không thuộc đơn")
        delay = H.db_delay_days(parcel, ctx.as_of)
        if (parcel.get("delay_cause") not in policy["fault_causes"]
                or parcel.get("carrier_id") != action.get("carrier_id")
                or delay < policy["late"]["min_days_fee"]
                or action.get("delay_days") != delay):
            return Verdict.deny("tracking không xác nhận lỗi của hãng cho kiện hàng này")

    if tool == "notify_carrier":
        payload_in = action.get("payload", {})
        order_id = action.get("order_id") or payload_in.get("order_id")
        order = ctx.tools.lookup_order(order_id)
        recorded = ctx.tools.fault_rows(ticket_id=action.get("ticket_id"), order_id=order_id)
        if (order is None or policy is None
                or not any(row.get("parcel_id") == payload_in.get("parcel_id")
                           and row.get("carrier_id") == action.get("carrier_id") for row in recorded)):
            return Verdict.deny("chỉ báo hãng sau khi đã ghi nhận lỗi hợp lệ")
        allowed = {"order_id", "parcel_id", "district", "delay_days"}
        allowed.intersection_update(policy.get("carrier_notice_fields", []))
        allowed.difference_update((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
        payload = {key: value for key, value in payload_in.items() if key in allowed}
        if payload != payload_in:
            return Verdict.modify("loại dữ liệu không được phép gửi cho bên thứ ba", payload=payload)

    return Verdict.allow()
