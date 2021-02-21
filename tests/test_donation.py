from matcher.donation import Donation
from matcher.exceptions import BadRequestException
import uuid
import pytest

@pytest.mark.order(100)
def test_donation_is_valid():
    """
    Test to see if donation objects are valid
    amount is float
    amount is > MIN_DONATION
    amount is < MAX_DONATION
    """

    donation_id = uuid.uuid4().hex
    amount = 100.00

    donation = Donation(donation_id, amount)

    assert isinstance(donation.amount, float)

@pytest.mark.order(102)
def test_donation_has_valid_amount_other():
    donation_id = uuid.uuid4().hex
    amount = "500g"

    with pytest.raises(ValueError):
        Donation(donation_id, amount)

@pytest.mark.order(103)
def test_donation_amount_min():
    donation_id = uuid.uuid4().hex
    amount = 4

    with pytest.raises(BadRequestException):
        Donation(donation_id, amount)

@pytest.mark.order(104)
def test_donation_amount_max():
    donation_id = uuid.uuid4().hex
    amount = 25001

    with pytest.raises(BadRequestException):
        Donation(donation_id, amount)