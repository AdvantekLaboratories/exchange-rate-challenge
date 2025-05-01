from datetime import datetime

class CurrencyData:
    def __init__(self, time: datetime, value: float) -> None:
        self.time = time
        self.value = value
