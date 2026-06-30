from pydantic import BaseModel

class AlphaVantageGlobalQuoteSchema(BaseModel):
    symbol:        str
    price:         str
    change:        str
    changePercent: str

class AlphaVantageTimeSeriesEntrySchema(BaseModel):
    open:   str
    high:   str
    low:    str
    close:  str
    volume: str
