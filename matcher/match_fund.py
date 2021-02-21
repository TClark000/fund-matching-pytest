from matcher.exceptions import BadRequestException

class MatchFund(object):

    def __init__(self, match_fund_id, total_amount, match_order, match_ratio=[1, 1]):

        self.match_fund_id = match_fund_id

        try:
            self.total_amount = float(total_amount)
        except TypeError as e:
            raise BadRequestException("Total amount cannot be expressed as a float, with error %s" % str(e))

        self.match_order = match_order
        self.matching_ratio = match_ratio

        self.matching_ratio_as_float_multiplier = self.matching_ratio[0] / self.matching_ratio[1]