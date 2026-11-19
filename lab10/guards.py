"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

Vòng 1: 3 cổng phòng ngừa rút từ B4 (HAZOP), B2 (T-002@55) và B6 (Pre-mortem).
"""
from . import helpers as H
from .tools import Verdict


def _current_policy(ctx):
    policies = ctx.tools.lookup_policies()
    return H.effective_policy(policies, ctx.as_of) or next(
        (p for p in policies if p.get("index_active")), policies[0]
    )


def pre_guard(ctx):
    """Cổng 1 (Pre-mortem & B3 drift): ghim đúng phiên bản chính sách hiệu lực theo ctx.as_of."""
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if pol is not None:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def _check_issue_refund(ctx, action):
    """Cổng 2: đối chiếu quyền lợi hoàn tiền với DB tracking, chính sách hiệu lực, duyệt & chống lặp."""
    if action.get("basis") == "fail_open":
        ctx.log("guard_block_fail_open", tool="issue_refund")
        return Verdict.escalate("chặn fail-open khi LLM quá tải: chuyển người duyệt")

    # Chống ghi lặp cùng ticket trong sổ cái (ví dụ khi LLM 429 gây write_retry)
    if ctx.tools.ledger_rows(ticket_id=action.get("ticket_id")):
        ctx.log("guard_block_duplicate_refund", ticket_id=action.get("ticket_id"))
        return Verdict.deny("ticket này đã có lệnh hoàn tiền trong sổ cái")

    order = ctx.tools.lookup_order(action.get("order_id"))
    pol = _current_policy(ctx)
    if order is None or pol is None:
        return Verdict.escalate("thiếu dữ liệu đơn hoặc chính sách hiệu lực")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    cause = parcel.get("delay_cause")
    entitled = H.entitlement_vnd(pol, order, delay, cause) if cause else 0

    if entitled <= 0:
        ctx.log("guard_deny_no_entitlement", db_delay=delay, cause=cause, asked=action.get("amount_vnd"))
        return Verdict.deny("đối chiếu tracking DB chưa đủ điều kiện hoàn tiền")

    if action.get("amount_vnd", 0) > entitled or action.get("payer", "LOGIX") != "LOGIX":
        ctx.log("guard_escalate_amount_mismatch", entitled=entitled, asked=action.get("amount_vnd"), payer=action.get("payer"))
        return Verdict.escalate("số tiền hoặc bên chịu tiền đề xuất lệch với chính sách DB")

    if action.get("amount_vnd", 0) > pol["auto_limit_vnd"]:
        aid = action.get("approval_id")
        cand = next((a for a in ctx.tools.lookup_approvals(approval_id=aid) if aid), None)
        valid = (
            cand is not None
            and cand.get("ticket_id") == action.get("ticket_id")
            and cand.get("status") == "valid"
            and cand.get("expires_at", "") >= ctx.as_of
            and cand.get("max_vnd", 0) >= action.get("amount_vnd", 0)
        )
        if not valid:
            ctx.log("guard_escalate_invalid_approval", approval_id=aid)
            return Verdict.escalate("vượt hạn mức tự động nhưng phê duyệt không hợp lệ")

    return Verdict.allow()


def _check_carrier_fault(ctx, action):
    """Cổng 3 (HAZOP B4): chỉ ghi lỗi hãng khi kiện giao trễ thật theo DB và có delay_cause hợp lệ."""
    order = ctx.tools.lookup_order(action.get("order_id"))
    pol = _current_policy(ctx)
    if order is None or pol is None:
        return Verdict.deny("thiếu dữ liệu đơn hoặc chính sách để ghi lỗi hãng")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    if not H.carrier_at_fault(pol, parcel, delay):
        ctx.log("guard_deny_carrier_fault", parcel_id=parcel["parcel_id"], db_delay=delay, cause=parcel.get("delay_cause"))
        return Verdict.deny("chưa đủ điều kiện ghi lỗi hãng theo tracking DB")

    if action.get("parcel_id") != parcel["parcel_id"] or action.get("carrier_id") != parcel["carrier_id"]:
        ctx.log("guard_fix_carrier_parcel", old_carrier=action.get("carrier_id"), new_carrier=parcel["carrier_id"])
        return Verdict.modify(
            "chỉnh đúng kiện và hãng gây trễ theo tracking DB",
            parcel_id=parcel["parcel_id"],
            carrier_id=parcel["carrier_id"],
            driver_id=parcel.get("driver_id"),
            delay_days=delay,
        )
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool == "issue_refund":
        return _check_issue_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _check_carrier_fault(ctx, action)
    return Verdict.allow()
