"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def guard_intervention_rate(trials):
    return sum(any(e.get("type") == "gate" and e.get("action") in ("deny", "escalate", "modify")
                   for e in t["events"]) for t in trials) / max(1, len(trials))


def tracking_delay_mismatch_rate(trials):
    """Fraction of trials where the model used a claimed delay that differed from tracking."""
    mismatches = 0
    for trial in trials:
        if any(
            event["type"] == "model_override"
            and event.get("field") == "delay_days"
            and event.get("db") is not None
            and event.get("ticket") is not None
            and event["db"] != event["ticket"]
            for event in trial["events"]
        ):
            mismatches += 1
    return mismatches / max(1, len(trials))


def missing_delay_cause_rate(trials):
    """Tỉ lệ lượt có giao trễ nhưng tracking DB chưa ghi nguyên nhân (`cause_recorded == False`)."""
    missing = sum(
        any(e.get("type") == "tracking" and e.get("cause_recorded") is False for e in t["events"])
        for t in trials
    )
    return missing / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "guard_intervention_rate": guard_intervention_rate,
    "tracking_delay_mismatch_rate": tracking_delay_mismatch_rate,
    "missing_delay_cause_rate": missing_delay_cause_rate,
}
STARTER_MONITORS = ("escalation_rate",)
