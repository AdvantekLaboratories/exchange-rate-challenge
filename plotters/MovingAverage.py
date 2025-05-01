from models import CurrencyData
from typing import List
import plotly.express as px

class MovingAverage:
    """Plotter for showing the moving average vs the current value.
    """
    def __init__(self, data: List[CurrencyData]):
        self.data = data
        
    def show(self) -> None:
        times  = [d.time  for d in self.data]
        values = [d.value for d in self.data]
        
        fig = px.line(x=times, y=values, labels={'x': "time", 'y': "HUF"})
        
        fig.show()