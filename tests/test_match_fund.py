from matcher.match_fund import MatchFund
import random
import uuid

def test_match_fund_is_valid():
    """
    Test to see if match fund objects are valid
    total_amount is float
    match_order is int
    matching_ratio is list

    """
    match_fund_id = uuid.uuid4().hex
    total_amount = 100000.5
    match_order = random.randint(0, 10)
    match_ratio = [2, 1]

    match_fund = MatchFund(match_fund_id, total_amount, match_order, match_ratio)

    assert isinstance(match_fund.total_amount, float)
    assert isinstance(match_fund.match_order, int)
    assert isinstance(match_fund.matching_ratio, list)
