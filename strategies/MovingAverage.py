from typing import List
from models import CurrencyData
import statistics

class MovingAverage:
    """Strategy for watching moving average and current value difference
    """
    def __init__(self, data: List[CurrencyData]):
        self.data = data
    
    @property
    def _average(self) -> float:
        return statistics.fmean([d.value for d in self.data])
    
    def show(self) -> None:
        days = (self.data[-1].time - self.data[0].time).days+1
        average = round(self._average, 2)
        current = self.data[0].value
        
        if current > average:
            recommend = "SELL"
        else:
            recommend = "BUY"

        print(f"""📊 {days}-day Moving Average: {average}
📈 Today's Rate: {current}
💡 Recommendation: {recommend}
""")