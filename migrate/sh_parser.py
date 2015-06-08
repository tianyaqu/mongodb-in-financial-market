import base_parser

class SHParser(base_parser.Parser):        
    @base_parser.decorator 
    def parse(self,json,day,exchange_id):
        self.data['ExchangeID'] = exchange_id
        self.data['TradingDay'] = day
        self.data['ActionDay'] = day
        self.data['SettlementPrice'] = '0'
        self.data['LastPrice'] = '0'
        self.data['OpenInterest'] = '0' 
        self.data['PreSettlementPrice'] = '0' 
        self.data['PreOpenInterest'] = '0'
        self.data['AveragePrice'] = '0'
        self.data['AveragePrice'] = '0'
        self.data['UpdateMillisec'] = self.data['UpdateTime'][-3:]
        self.data['UpdateTime'] = self.data['UpdateTime'][:-3]