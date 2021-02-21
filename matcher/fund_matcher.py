from collections import OrderedDict
from matcher.allocation import Allocation
from matcher.exceptions import BadRequestException
from datetime import datetime

MAX_RESERVED_AMOUNT = 25000.00
MIN_RESERVED_AMOUNT = 5.00

MAX_MATCHED_AMOUNT = 25000.00
MIN_MATCHED_AMOUNT = 5.00

MIN_DONATION_AMOUNT = 5.00
MAX_DONATION_AMOUNT = 25000.00

# Valid statuses
RESERVED = "Reserved"
COLLECTED = "Collected"
EXPIRED = "Expired"

class FundMatcher(object):

    def __init__(self, match_funds):
        """
        Core algorithm to match donation to matchfunds
        Instantiated with an ordered dict of match funds
        """

        match_funds.sort(reverse=False, key=lambda x: x.match_order)
        self.match_funds = OrderedDict([(mf.match_fund_id, mf) for mf in match_funds])

        self.allocation_state = {}

    def get_match_funds_as_list(self):

        return list(self.match_funds.values())

    def reserve_funds(self, donation):
        """
        Method takes a Donation object and reserves this donation against match funds
        Depending on the funds availale in the match_fund, the donation is either fully,
        partially matched. or not matched at all.
        The match_fund_state is updated with the result.
        Assuming that donation id of a donation is unique
        """
        donation_balance = donation.amount

        allocations = []
        for match_fund in self.match_funds.values():
            matching_amount_required = donation_balance * (match_fund.matching_ratio_as_float_multiplier)

            if match_fund.total_amount == 0:
                # fund is exhausted - move on to next match_fund
                continue

            if match_fund.total_amount >= matching_amount_required:
                # full match
                allocation = Allocation(match_fund.match_fund_id, matching_amount_required, RESERVED)
                allocations.append(allocation)
                donation_balance = 0
                match_fund.total_amount -= matching_amount_required
                break

            else:
                # partial match
                matched_allocated_amount = matching_amount_required - match_fund.total_amount
                allocation = Allocation(match_fund.match_fund_id, match_fund.total_amount, RESERVED)
                allocations.append(allocation)
                donation_balance -= (matching_amount_required - matched_allocated_amount) / match_fund.matching_ratio_as_float_multiplier
                match_fund.total_amount = 0
            
            if donation_balance == 0:
                # donation has been matched completely - break from for
                break

        allocation_state_doc = {
            'allocations': allocations,
            'created_time': datetime.now(),
            'updated_time': datetime.now(),
            'original_donation': donation.amount,
            'donation_balance_unmatched': donation_balance,
            'overall_status': RESERVED
        }
        self.allocation_state[donation.donation_id] = allocation_state_doc