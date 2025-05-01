import requests
from datetime import datetime
import csv
from io import StringIO

from typing import List

from models.CurrencyData import CurrencyData

class OTP(requests.Session):
    """provider for OTP Bank (otpbank.hu)
    """
    #example: https://www.otpbank.hu/apps/exchangerate/api/exchangerate/otp/2025-04-30
    REALTIME_URL = "https://www.otpbank.hu/apps/exchangerate/api/exchangerate/otp/{}"
    #example: https://www.otpbank.hu/apps/exchangerate/api/downloads/csv/2025-04-22/2025-04-30?currencies=EUR&lang=HU
    HISTORY_URL  = "https://www.otpbank.hu/apps/exchangerate/api/downloads/csv/{}/{}?currencies={}&lang={}"
    
    code: str
    
    def __init__(self, code: str) -> None:
        super().__init__()
        self.code = code
    
    def _parse_csv(self, text: str) -> List[List[str]]:
        f = StringIO(text)
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
            
        return list(reader)
    
    @property
    def _today(self) -> str:
        return self._format_date(datetime.today())
    
    @staticmethod
    def _format_date(date: datetime) -> str:
        return date.strftime("%Y-%m-%d")
    
    def current(self) -> CurrencyData:
        r = self.get(self.REALTIME_URL.format(self._today))
        r.raise_for_status()
        
        rates = r.json()['dates'][0]['versions'][0]['exchangeRates']
        
        rate = [r for r in rates if r['currencyCode'] == self.code]
        
        if len(rate) == 0:
            raise ValueError(f"Currency {self.code} not supported by this provider: {self.__class__.__name__}")
        
        return CurrencyData(datetime.now(), rate[0]['middleRate'])
    
    def history(self, from_: datetime, to: datetime) -> List[CurrencyData]:
        text = self.get(self.HISTORY_URL.format(
            self._format_date(from_),
            self._format_date(to),
            self.code,
            "HU")).text
        
        # first 2 lines are headers
        csv_text = text.split('\n', 2)[-1]
        
        csv_data = self._parse_csv(csv_text)
        
        data = [CurrencyData(datetime.strptime(r[1], "%Y.%m.%d %H:%M"), float(r[3].replace(',', '.'))) for r in csv_data]
        
        return data