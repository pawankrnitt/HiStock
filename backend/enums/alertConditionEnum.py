# enums/alertConditionEnum.py
from enum import Enum

class AlertConditionEnum(str, Enum):
    PRICE_ABOVE = "price_above"
    PRICE_BELOW = "price_below"
