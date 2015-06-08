import base_parser

class CFFEX_Parser(base_parser.Parser):        
    @base_parser.decorator 
    def parse(self,json,day,exchange_id):
        self.data['ExchangeID'] = exchange_id
        self.data['TradingDay'] = day
        self.data['ActionDay'] = day
        #self.data['SettlementPrice'] = 0
        self.data['UpdateMillisec'] = self.data['UpdateTime'][-3:]
        self.data['UpdateTime'] = self.data['UpdateTime'][:-3]