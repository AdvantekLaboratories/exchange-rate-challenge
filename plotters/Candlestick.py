from models import CurrencyData
from typing import List
import plotly.graph_objects as go

class Candlestick:
    """Plotter for a candlestick graph in daily breakdown.
    """
    def __init__(self, data: List[CurrencyData]):
        self.data = data    
    
    def show(self) -> None:
        data = {
            'date'  :[],
            'open'  :[],
            'high'  :[],
            'low'   :[],
            'close' :[],
        }
        
        for d in self.data:
            if d.time.date() not in data['date']:
                data['date'].append(d.time.date())
            
        for date in data['date']:
            values = [d.value for d in self.data if d.time.date() == date]
            data['open' ].append(values[0])
            data['high' ].append(max(values))
            data['low'  ].append(min(values))
            data['close'].append(values[-1])
         
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x     = data['date'],
                    open  = data['open'],
                    high  = data['high'],
                    low   = data['low'],
                    close = data['close']
                    )
                ]
            )

        fig.show()
