class Allocation(object):

    def __init__(self, match_fund_id, match_fund_allocation, status):
        self.match_fund_id = match_fund_id
        self.match_fund_allocation = match_fund_allocation
        self.status = status

    def to_dict(self):
        return {
            "match_fund_id": self.match_fund_id,
            "match_fund_allocation": self.match_fund_allocation,
            "status": self.status
        }