from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class ContractType(StrEnum):
    MONTH_TO_MONTH = "month-to-month"
    ONE_YEAR = "one-year"
    TWO_YEAR = "two-year"


class CustomerFeatures(BaseModel):
    tenure_months: int = Field(ge=0, le=120)
    monthly_spend: float = Field(ge=0, le=10000)
    support_tickets: int = Field(ge=0, le=500)
    contract_type: ContractType

    @field_validator("monthly_spend")
    @classmethod
    def finite_spend(cls, value: float) -> float:
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("monthly_spend must be finite")
        return value


class TrainingRow(CustomerFeatures):
    churn: int = Field(ge=0, le=1)


class PredictionResponse(BaseModel):
    prediction: int
    probability: float = Field(ge=0, le=1)
    model_version: str
    request_id: str
