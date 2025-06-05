from scripts.risk import calc_contracts


def test_calc_contracts_zero_alpha():
    assert calc_contracts(10000, 10, 0.0) == 0
