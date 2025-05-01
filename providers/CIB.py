import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List

from models import CurrencyData

class CIB(requests.Session):
    """Provider for CIB Bank (cib.hu)
    """
    REALTIME_URL = "https://net.cib.hu/kis_kozep_nagy_vallalatok/arfolyamok/"
    HISTORY_URL  = "https://net.cib.hu/kis_kozep_nagy_vallalatok/arfolyamok/archiv/index"
    
    code: str
    
    def __init__(self, code: str) -> None:
        super().__init__()
        self.code = code
        
    @staticmethod
    def _format_date(date: datetime) -> str:
        return date.strftime("%Y-%m-%d")
        
    def current(self) -> CurrencyData:
        r = self.get(self.REALTIME_URL)
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        rows = soup.find(id="contentArea").find_all("table")[1].find_all('tr')[1:]
        
        rate = [r for r in rows if r.find_all("td")[0].string == self.code]
        
        if len(rate) == 0:
            raise ValueError(f"Currency {self.code} not supported by this provider: {self.__class__.__name__}")
        
        data = CurrencyData(datetime.now(), float(rate[0].find_all('td')[3].text))
        
        return data
        
    def history(self, from_: datetime, to: datetime) -> List[CurrencyData]:
        r = self.post(self.HISTORY_URL, 
                      data= {
                                'ru_type': 'valarf',
                                'ru_date_from': self._format_date(from_), 
                                'ru_date_to': self._format_date(to),
                                f'curr_{self.code}': '1',
                                'sendForm': ''
                            }
                      )
        
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        #first 2 rows are headers
        trs = soup.find(id='contentArea').div.div.div.table.find_all("tr")[2:-1]
        
        rates = []
        for tr in trs:
            tds = tr.find_all('td')
            rates.append(
                CurrencyData(
                    datetime.strptime(tds[0].text + ' ' + tds[4].text[-6:-1], "%Y-%m-%d %H:%M"), 
                    float(tds[2].text)
                    )
                )
            
        return sorted(rates, key = lambda x: x.time)
            
        