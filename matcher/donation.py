from matcher.exceptions import BadRequestException

MIN_DONATION = 5.00
MAX_DONATION = 25000.00

class Donation(object):

    def __init__(self, donation_id, amount):
        self.donation_id = donation_id
        
        try:
            self.amount = float(amount)
        except TypeError as e:
            raise BadRequestException("Amount cannot be expressed as a float, with error %s" % str(e))

        if self.amount < MIN_DONATION:
            raise BadRequestException("Donation amount is too small, %s" % amount)

        if self.amount > MAX_DONATION:
            raise BadRequestException("Donation amount is too high, %s" % amount)




