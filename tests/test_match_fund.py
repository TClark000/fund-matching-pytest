from matcher.match_fund import MatchFund
import random
import uuid
import pytest

def test_match_fund_is_valid():
    """
    Test to see if match fund objects are valid
    total_amount is float
    match_order is int
    matching_ratio is list
    matching_ratio has a len of 2
    matching_ratio lh rh are persistent
    matching_ratio defaults 1:1
    """
    match_fund_id = uuid.uuid4().hex
    total_amount = 100000.5
    match_order = random.randint(0, 10)
    match_ratio = [2, 1]

    match_fund = MatchFund(match_fund_id, total_amount, match_order, match_ratio)

    assert isinstance(match_fund.total_amount, float)
    assert isinstance(match_fund.match_order, int)
    assert isinstance(match_fund.matching_ratio, list)

    match_ratio = match_fund.matching_ratio

    assert len(match_ratio) == 2
    lhs, rhs = match_ratio
    assert lhs == 2
    assert rhs == 1

    another_match_fund = MatchFund(match_fund_id, total_amount, match_order)
    lhs, rhs = another_match_fund.matching_ratio
    assert lhs == 1
    assert rhs == 1

def test_match_fund_total_amount_other():
    match_fund_id = uuid.uuid4().hex
    total_amount = "500g"
    match_order = random.randint(0, 10)

    with pytest.raises(ValueError):
        MatchFund(match_fund_id, total_amount, match_order)