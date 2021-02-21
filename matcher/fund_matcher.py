from collections import OrderedDict
from matcher.exceptions import BadRequestException

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

    def get_match_funds_as_list(self):

        return list(self.match_funds.values())
