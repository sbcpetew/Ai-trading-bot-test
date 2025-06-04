"""Risk and money management utilities."""


def calc_contracts(
    equity: float, stop_ticks: int, alpha: float, kelly: float = 1.0
) -> int:
    stop_tick_value = stop_ticks * 12.50
    max_risk = 0.02 * equity
    contracts = int(
        min(alpha * kelly * 0.25 * equity / stop_tick_value, max_risk / stop_tick_value)
    )
    return max(1, contracts)
