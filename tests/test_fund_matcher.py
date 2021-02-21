from matcher.match_fund import MatchFund
from matcher.fund_matcher import FundMatcher
from matcher.fund_matcher import RESERVED, COLLECTED, EXPIRED
from matcher.donation import Donation
from matcher.exceptions import BadRequestException

import pytest

@pytest.fixture
def simple_match_funds():
    """
    fixture simple fund array without ratios
    """

    example_funds_data = [[
        "fund_1",  # id
        100.00,  # amount
        3,  # order
    ], [
        "fund_2",
        100.00,
        7
    ], [
        "fund_3",
        100.00,
        1,
    ]
    ]

    return [MatchFund(*ef) for ef in example_funds_data]

@pytest.fixture
def match_funds_with_ratios():
    example_funds_data = [[
        "fund_1",  # id
        100.00,  # amount
        3,  # order
        [1, 1]  # ratio
    ], [
        "fund_2",
        100.00,
        7,
        [2, 1]
    ], [
        "fund_3",
        100.00,
        1,
        [1, 1]
    ]
    ]

    return [MatchFund(*ef) for ef in example_funds_data]

def test_match_funds_are_sorted_by_match_order_correctly(simple_match_funds):

    fund_matcher = FundMatcher(simple_match_funds)

    correct_match_order = [1, 3, 7]

    for ix, mf in enumerate(fund_matcher.get_match_funds_as_list()):
        assert mf.match_order == correct_match_order[ix]

def test_simple_reserve_full_match(match_funds_with_ratios):

    fund_matcher = FundMatcher(match_funds_with_ratios)

    donation = Donation("donation_1", 50)

    fund_matcher.reserve_funds(donation)

    state = fund_matcher.allocation_state

    allocations = state[donation.donation_id]['allocations']

    assert (len(allocations) == 1)
    assert (allocations[0].match_fund_id == "fund_3")
    # assert (allocations[0].match_fund_id == "fund_1")