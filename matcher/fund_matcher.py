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

    def collect_donation(self, donation_id):
        """
        Collect a donation that is set to Reserved
        Sets the state of all allocations against that donation are set to Collected
        Throws errors if the allocation status is not Reserved
        """

        # Is donation_id valid?
        if not donation_id in self.allocation_state:
            raise BadRequestException("Invalid donation id %s" % donation_id)

        allocations = self.allocation_state[donation_id]['allocations']

        # Ensure that only allocation status of RESERVED are COLLECTED
        for allocation in allocations:
            if not allocation.status == RESERVED:
                raise BadRequestException("Invalid collection request. Allocation is not reserved")
            else:
                allocation.status = COLLECTED

        self.allocation_state[donation_id]['allocations'] = allocations
        self.allocation_state[donation_id]['updated_time'] = datetime.now()
        self.allocation_state[donation_id]['overall_status'] = COLLECTED
    
    def expire_donation(self, donation_id):
        """
        Expire a donation
        Finds the donation based on id, checks to see if is RESERVED.
        If it is, then set the status to EXPIRED and return the matched funds
        so that new donations can use them.
        Note: the instructions mention not to do this for previously collected donations - but
        not new donations.
        """

        if donation_id not in self.allocation_state:
            raise BadRequestException("Invalid donation_id %s" % donation_id)

        allocations = self.allocation_state[donation_id]['allocations']

        for allocation in allocations:
            if not allocation.status == RESERVED:
                raise BadRequestException("Invalid collection request. Allocation is not reserved")
            else:
                allocation.status = EXPIRED
                allocation_match_fund = self.match_funds[allocation.match_fund_id]
                allocation_match_fund.total_amount += allocation.match_fund_allocation
                self.match_funds[allocation.match_fund_id] = allocation_match_fund

        self.allocation_state[donation_id]['allocations'] = allocations
        self.allocation_state[donation_id]['updated_time'] = datetime.now()
        self.allocation_state[donation_id]['overall_status'] = EXPIRED

    def list_match_fund_allocations(self):
        """
        Only list RESERVED or COLLECTED allocations
        Returns the allocations
        """

        all_allocations = []

        for donation_id in self.allocation_state.keys():
            if self.allocation_state[donation_id]['overall_status'] != EXPIRED:
                output_doc = {
                    'donation_id': donation_id,
                    **self.allocation_state[donation_id]
                }
                allocations = [a.to_dict() for a in self.allocation_state[donation_id]['allocations']]
                output_doc['allocations'] = allocations
                all_allocations.append(output_doc)

        return all_allocations