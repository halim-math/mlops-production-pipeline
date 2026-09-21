import pytest
from pydantic import ValidationError

from mlops_pipeline.data.schema import CustomerFeatures


def test_valid_customer_contract() -> None:
    row = CustomerFeatures(
        tenure_months=12,
        monthly_spend=99.9,
        support_tickets=2,
        contract_type="one-year",
    )
    assert row.tenure_months == 12


def test_negative_spend_is_rejected() -> None:
    with pytest.raises(ValidationError):
        CustomerFeatures(
            tenure_months=12,
            monthly_spend=-1,
            support_tickets=2,
            contract_type="one-year",
        )
