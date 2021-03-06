from matcher.allocation import Allocation
from matcher.match_fund import MatchFund
from matcher.fund_matcher import FundMatcher
from matcher.fund_matcher import RESERVED, COLLECTED, EXPIRED
from matcher.donation import Donation
from matcher.exceptions import BadRequestException

import pytest

@pytest.fixture
def simple_match_funds():
    """
    fixture simple fund array without ratios (as default)
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
    """
    fixture fund arrays with ratios
    """

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

@pytest.fixture
def more_match_funds_with_ratios():
    """
    additional fixture fund arrays with ratios
    """

    example_funds_data = [[
        "fund_1",  # id
        100.00,  # amount
        3,  # order
        [2, 1]  # ratio
    ], [
        "fund_2",
        100.00,
        7,
        [3, 1]
    ], [
        "fund_3",
        100.00,
        1,
        [2, 1]
    ]
    ]
    return [MatchFund(*ef) for ef in example_funds_data]

@pytest.mark.order(301)
def test_match_funds_are_sorted_by_match_order_correctly(simple_match_funds):
    """
    Assert test to confirm ordered match fund array
    """

    fund_matcher = FundMatcher(simple_match_funds)

    correct_match_order = [1, 3, 7]

    for ix, mf in enumerate(fund_matcher.get_match_funds_as_list()):
        assert mf.match_order == correct_match_order[ix]

@pytest.mark.order(302)
def test_simple_reserve_full_match(match_funds_with_ratios):
    """
    reservation test will a full match on 1 fund
    """
    fund_matcher = FundMatcher(match_funds_with_ratios)

    donation = Donation("donation_1", 50)

    fund_matcher.reserve_funds(donation)

    state = fund_matcher.allocation_state

    allocations = state[donation.donation_id]['allocations']

    assert (len(allocations) == 1)
    assert (allocations[0].match_fund_id == "fund_3")
    # assert (allocations[0].match_fund_id == "fund_1")

@pytest.mark.order(303)
def test_simple_reserve_partial_match(match_funds_with_ratios):
    """
    reservation test, donations allocated to > than 1 fund (partial)
    test donation is allocated in match_fund order
    """
    fund_matcher = FundMatcher(match_funds_with_ratios)

    donation = Donation("donation_1", 130)
    # donation = Donation("donation_1", 250)

    fund_matcher.reserve_funds(donation)

    state = fund_matcher.allocation_state

    allocations = state[donation.donation_id]['allocations']

    assert (len(allocations) == 2)
    assert (allocations[0].match_fund_id == "fund_3")
    assert (allocations[1].match_fund_id == "fund_1")
    # assert (allocations[2].match_fund_id == "fund_2")

@pytest.mark.order(304)
def test_reserve_full_match_with_ratios(match_funds_with_ratios):
    """
    reservation test, donations allocated to 1 fund
    test ratio of 2:1, match_fund allocation is doubled
    """

    fund_matcher = FundMatcher([match_funds_with_ratios[1]])

    donation = Donation("donation_1", 25)

    fund_matcher.reserve_funds(donation)

    state = fund_matcher.allocation_state

    allocations = state[donation.donation_id]['allocations']
    match_funds = fund_matcher.get_match_funds_as_list()

    assert (len(allocations) == 1)
    assert (allocations[0].match_fund_id == "fund_2")
    assert (match_funds[0].total_amount == 50)

@pytest.mark.order(305)
def test_reserve_partial_match_with_ratios(more_match_funds_with_ratios):
    """
    reservation test, donations allocated to 2 fund
    test order of match_fund allocation
    test ratio of 2:1, match_fund allocation is doubled
    test first fund is exhausted
    test second fund remaining total_amount
    """
    fund_matcher = FundMatcher(more_match_funds_with_ratios)

    donation = Donation("donation_1", 60)

    fund_matcher.reserve_funds(donation)

    state = fund_matcher.allocation_state

    allocations = state[donation.donation_id]['allocations']
    match_funds = fund_matcher.get_match_funds_as_list()

    assert (len(allocations) == 2)
    assert (allocations[0].match_fund_id == "fund_3")
    assert (allocations[1].match_fund_id == "fund_1")
    assert (match_funds[0].total_amount == 0)
    assert (match_funds[1].total_amount == 80)

@pytest.mark.order(306)
def test_reserve_full_match_multiple_donations(simple_match_funds):
    """
    reservation test, donations allocated to 2 fund
    test order of match_fund allocation
    test first fund is exhausted
    test second fund remaining total_amount
    ratio defaults to 1:1
    """
    fund_matcher = FundMatcher(simple_match_funds)

    donation_1 = Donation("donation_1", 110)
    donation_2 = Donation("donation_2", 50)

    fund_matcher.reserve_funds(donation_1)
    fund_matcher.reserve_funds(donation_2)

    state = fund_matcher.allocation_state
    allocations_1 = state[donation_1.donation_id]['allocations']
    allocations_2 = state[donation_2.donation_id]['allocations']
    match_funds = fund_matcher.get_match_funds_as_list()

    assert (len(allocations_1) == 2)
    assert (len(allocations_2) == 1)

    assert (match_funds[0].total_amount == 0)
    assert (match_funds[1].total_amount == 40)

@pytest.mark.order(307)
def test_status_on_reserved_funds(simple_match_funds):
    """
    test allocations are RESERVED
    test allocations are RESERVED if match_funds exhausted
    """
    fund_matcher = FundMatcher(simple_match_funds)
    donation_1 = Donation("donation_1", 110)
    donation_2 = Donation("donation_2", 140)
    donation_3 = Donation("donation_3", 180)

    fund_matcher.reserve_funds(donation_1)
    fund_matcher.reserve_funds(donation_2)
    fund_matcher.reserve_funds(donation_3)

    state = fund_matcher.allocation_state
    allocations_1 = state[donation_1.donation_id]['allocations']
    allocations_2 = state[donation_2.donation_id]['allocations']
    allocations_3 = state[donation_2.donation_id]['allocations']

    for a in allocations_1:
        assert a.status == RESERVED

    for a in allocations_2:
        assert a.status == RESERVED

    for a in allocations_3:
        assert a.status == RESERVED

@pytest.mark.order(308)
def test_reserve_funds_donation_balance_unmatched(simple_match_funds):
    """
    test allocations are RESERVED
    test allocations are RESERVED if match_funds exhausted
    test original_donation & donation_balance_unmatched
    """
    fund_matcher = FundMatcher(simple_match_funds)
    donation_1 = Donation("donation_1", 150)
    donation_2 = Donation("donation_2", 250)

    fund_matcher.reserve_funds(donation_1)
    fund_matcher.reserve_funds(donation_2)

    state = fund_matcher.allocation_state
    allocations_1 = state[donation_1.donation_id]['allocations']
    allocations_2 = state[donation_2.donation_id]['allocations']

    for a in allocations_1:
        assert a.status == RESERVED

    for a in allocations_2:
        assert a.status == RESERVED
    
    assert state[donation_1.donation_id]['original_donation'] == 150
    assert state[donation_1.donation_id]['donation_balance_unmatched'] == 0
    assert state[donation_2.donation_id]['original_donation'] == 250
    assert state[donation_2.donation_id]['donation_balance_unmatched'] == 100

@pytest.mark.order(309)
def test_simple_collect_donation(simple_match_funds):
    """
    test allocation status set to COLLECTED
    """
    fund_matcher = FundMatcher(simple_match_funds)
    donation = Donation("donation_1", 50)

    fund_matcher.reserve_funds(donation)
    fund_matcher.collect_donation(donation.donation_id)

    state = fund_matcher.allocation_state
    allocations = state[donation.donation_id]['allocations']

    for a in allocations:
        assert a.status == COLLECTED

@pytest.mark.order(310)
def test_simple_collect_multiple_donations(simple_match_funds):
    """
    test allocations status set to COLLECTED
    test overall status set to COLLECTED
    test match_fund total balance (occurs when reservations are allocated)
    """
    fund_matcher = FundMatcher(simple_match_funds)
    donation_1 = Donation("donation_1", 110)
    donation_2 = Donation("donation_2", 50)

    fund_matcher.reserve_funds(donation_1)
    fund_matcher.reserve_funds(donation_2)

    fund_matcher.collect_donation(donation_1.donation_id)
    fund_matcher.collect_donation(donation_2.donation_id)

    state = fund_matcher.allocation_state
    allocations_1 = state[donation_1.donation_id]['allocations']
    allocations_2 = state[donation_2.donation_id]['allocations']

    for a in allocations_1:
        assert a.status == COLLECTED

    for a in allocations_2:
        assert a.status == COLLECTED

    assert state[donation_1.donation_id]['overall_status'] == COLLECTED
    assert state[donation_2.donation_id]['overall_status'] == COLLECTED

    match_funds = fund_matcher.get_match_funds_as_list()

    assert match_funds[0].total_amount == 0
    assert match_funds[1].total_amount == 40

@pytest.mark.order(311)
def test_simple_collect_donation_wrong_id(simple_match_funds):
    """
    Tests collection donation_id is valid 
    """
    fund_matcher = FundMatcher(simple_match_funds)
    donation = Donation("donation_1", 50)

    fund_matcher.reserve_funds(donation)

    with pytest.raises(BadRequestException):
        fund_matcher.collect_donation("donation_10")

@pytest.mark.order(312)
def test_expire_donation_check_status_and_fund_balance(simple_match_funds):
    """
    test allocations are EXPIRED
    test overall status is EXPIRED
    test match_fund total_balance remunerated
    """
    fund_matcher = FundMatcher(simple_match_funds)
    donation = Donation("donation_1", 50)

    fund_matcher.reserve_funds(donation)

    fund_matcher.expire_donation(donation.donation_id)

    state = fund_matcher.allocation_state

    allocations = state[donation.donation_id]['allocations']

    for a in allocations:
        assert a.status == EXPIRED
    assert state[donation.donation_id]['overall_status'] == EXPIRED

    match_funds = fund_matcher.get_match_funds_as_list()
    assert (match_funds[0].total_amount == 100)

@pytest.mark.order(313)
def test_expire_donation_on_invalid_status(simple_match_funds):
    """
    test allocation state that is set to COLLECTED is not EXPIRED
    """
    fund_matcher = FundMatcher(simple_match_funds)
    donation = Donation("donation_1", 50)

    fund_matcher.reserve_funds(donation)
    fund_matcher.collect_donation(donation.donation_id)

    with pytest.raises(BadRequestException):
        fund_matcher.expire_donation(donation.donation_id)

@pytest.mark.order(314)
def test_list_match_fund_allocations(simple_match_funds):
    """
    Only list RESERVED or COLLECTED allocations (ignores EXPIRED)
    Returns a list of allocations per donation in the format:
    { "donation_id" : <donation_id>,
        "allocations" : [ { "match_fund_id": <fund_id>, "match_fund_allocation": <amount>, "status": <status>}, {..} ],
        "created_time": datetime when reservation was first created,
        "updated_time": datetime when reservation was last updated,
        "overall_status": one of "Reserved" or "Collected",
        "donation_balance_unmatched": <amount of donation unmatched>,
        "original_donation": <the original donation amount>
    }
    """

    fund_matcher = FundMatcher(simple_match_funds)
    donation_1 = Donation("donation_1", 100)
    donation_2 = Donation("donation_2", 250)
    donation_3 = Donation("donation_3", 45)

    fund_matcher.reserve_funds(donation_1)
    fund_matcher.reserve_funds(donation_2)
    fund_matcher.reserve_funds(donation_3)

    fund_matcher.collect_donation(donation_2.donation_id)
    fund_matcher.expire_donation(donation_3.donation_id)

    allocations_list = fund_matcher.list_match_fund_allocations()

    min_expected_output = [
        {
            "donation_id": "donation_1",
            "allocations": [
                {"match_fund_id": "fund_3",
                "match_fund_allocation": 100,
                "status": RESERVED
                }

            ],
        },
        {
            "donation_id": "donation_2",
            "allocations": [
                {"match_fund_id": "fund_1",
                "match_fund_allocation": 100,
                "status": COLLECTED
                },
                {"match_fund_id": "fund_2",
                "match_fund_allocation": 100,
                "status": COLLECTED
                }
            ],
            "original_donation": 250,
            "donation_balance_unmatched": 50,
            "overall_status": COLLECTED
        }
    ]

    assert len(min_expected_output) == len(allocations_list)
    assert allocations_list[0]['donation_id'] == min_expected_output[0]['donation_id']
    assert allocations_list[0]['allocations'] == min_expected_output[0]['allocations']
    assert allocations_list[1]['donation_id'] == min_expected_output[1]['donation_id']
    assert allocations_list[1]['allocations'] == min_expected_output[1]['allocations']