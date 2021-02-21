from matcher.donation import Donation
import uuid
import pytest

def test_donation_is_valid():
    """
    Test to see if donation objects are valid
    amount is float
    """

    donation_id = uuid.uuid4().hex
    amount = 100.00

    donation = Donation(donation_id, amount)

    assert isinstance(donation.amount, float)