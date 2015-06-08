import ConfigParser
import datetime

def decorator(func):
    def _decorator(self, *args, **kwargs):
        self.pre_parse(*args, **kwargs)
        func(self, *args, **kwargs)
    return _decorator

class Parser():
    def __init__(self,conf_name):
        self.load_conf(conf_name)
        self.day = "19700101"

    def load_conf(self,conf_name):
        self.mapper = {}
        cf = ConfigParser.ConfigParser()
        cf.read(conf_name)
        self.str_am_open = cf.get("time", "am_open")
        self.str_am_close = cf.get("time", "am_close")
        self.str_pm_open = cf.get("time", "pm_open")
        self.str_pm_close = cf.get("time", "pm_close")        
        self.market = cf.get("market", "name")
        self.ip = cf.get("database", "ip")
        self.port = cf.get("database", "port")
        self.mapper['ActionDay'] = cf.get("mapping", "ActionDay")
        self.mapper['TradingDay'] = cf.get("mapping", "TradingDay")
        self.mapper['AskPrice1'] = cf.get("mapping", "AskPrice1")
        self.mapper['AskPrice2'] = cf.get("mapping", "AskPrice2")
        self.mapper['AskPrice3'] = cf.get("mapping", "AskPrice3")
        self.mapper['AskPrice4'] = cf.get("mapping", "AskPrice4")
        self.mapper['AskPrice5'] = cf.get("mapping", "AskPrice5")
        self.mapper['AskVolume1'] = cf.get("mapping", "AskVolume1")
        self.mapper['AskVolume2'] = cf.get("mapping", "AskVolume2")
        self.mapper['AskVolume3'] = cf.get("mapping", "AskVolume3")
        self.mapper['AskVolume4'] = cf.get("mapping", "AskVolume4")
        self.mapper['AskVolume5'] = cf.get("mapping", "AskVolume5")
        self.mapper['AveragePrice'] = cf.get("mapping", "AveragePrice")
        self.mapper['BidPrice1'] = cf.get("mapping", "BidPrice1")
        self.mapper['BidPrice2'] = cf.get("mapping", "BidPrice2")
        self.mapper['BidPrice3'] = cf.get("mapping", "BidPrice3")
        self.mapper['BidPrice4'] = cf.get("mapping", "BidPrice4")
        self.mapper['BidPrice5'] = cf.get("mapping", "BidPrice5")
        self.mapper['BidVolume1'] = cf.get("mapping", "BidVolume1")
        self.mapper['BidVolume2'] = cf.get("mapping", "BidVolume2")
        self.mapper['BidVolume3'] = cf.get("mapping", "BidVolume3")
        self.mapper['BidVolume4'] = cf.get("mapping", "BidVolume4")
        self.mapper['BidVolume5'] = cf.get("mapping", "BidVolume5")
        self.mapper['ClosePrice'] = cf.get("mapping", "ClosePrice")
        self.mapper['ExchangeID'] = cf.get("mapping", "ExchangeID")
        self.mapper['HighestPrice'] = cf.get("mapping", "HighestPrice")
        self.mapper['InstrumentID'] = cf.get("mapping", "InstrumentID")
        self.mapper['LastPrice'] = cf.get("mapping", "LastPrice")
        self.mapper['LowerLimitPrice'] = cf.get("mapping", "LowerLimitPrice")
        self.mapper['LowestPrice'] = cf.get("mapping", "LowestPrice")
        self.mapper['OpenInterest'] = cf.get("mapping", "OpenInterest")
        self.mapper['OpenPrice'] = cf.get("mapping", "OpenPrice")
        self.mapper['PreClosePrice'] = cf.get("mapping", "PreClosePrice")
        self.mapper['PreOpenInterest'] = cf.get("mapping", "PreOpenInterest")
        self.mapper['PreSettlementPrice'] = cf.get("mapping", "PreSettlementPrice")
        self.mapper['SettlementPrice'] = cf.get("mapping", "SettlementPrice")
        self.mapper['Symbol'] = cf.get("mapping", "Symbol")
        self.mapper['TradingDay'] = cf.get("mapping", "TradingDay")
        self.mapper['Turnover'] = cf.get("mapping", "Turnover")
        self.mapper['UpdateMillisec'] = cf.get("mapping", "UpdateMillisec")
        self.mapper['UpdateTime'] = cf.get("mapping", "UpdateTime")
        self.mapper['UpperLimitPrice'] = cf.get("mapping", "UpperLimitPrice")
        self.mapper['Volume'] = cf.get("mapping", "Volume")

    def pre_parse(self,json,day,exchange_id):
        self.data = {}
        for item in self.mapper.iteritems():
            if item[1] != '0':
                self.data[item[0]] = json[item[1]]
            else:
                self.data[item[0]] = '0'

        self.validate()
        
    # do some tricks here    
    def validate(self):
        pass
        
    def to_str(self):
        return  '' + self.data['TradingDay'] + self.data['UpdateTime'] + self.data['UpdateMillisec'] + \
            ',' + self.data['Symbol'] + ',' + self.data['OpenPrice'] + \
            ',' + self.data['ClosePrice'] + ',' + self.data['HighestPrice'] + ',' + self.data['LowestPrice'] + ',' + self.data['Turnover'] + \
            ',' + self.data['Volume'] + ',' + self.data['LastPrice'] + ',' + self.data['AveragePrice'] + ',' + self.data['PreClosePrice'] + \
            ',' + self.data['UpperLimitPrice'] + ',' + self.data['LowerLimitPrice'] + ',' + self.data['OpenInterest'] + ',' + self.data['PreOpenInterest'] + \
            ',' + self.data['PreSettlementPrice'] + ',' + self.data['SettlementPrice'] + ',' + self.data['AskPrice1'] + ',' + self.data['AskPrice2'] + \
            ',' + self.data['AskPrice3'] + ',' + self.data['AskPrice4'] + ',' + self.data['AskPrice5'] + ',' + self.data['AskVolume1'] + \
            ',' + self.data['AskVolume2'] + ',' + self.data['AskVolume3'] + ',' + self.data['AskVolume4'] + ',' + self.data['AskVolume5'] + \
            ',' + self.data['BidPrice1'] + ',' + self.data['BidPrice2'] + ',' + self.data['BidPrice3'] + ',' + self.data['BidPrice4'] + \
            ',' + self.data['BidPrice5'] + ',' + self.data['BidVolume1'] + ',' + self.data['BidVolume2'] + ',' + self.data['BidVolume3'] + \
            ',' + self.data['BidVolume4'] + ',' + self.data['BidVolume5'] + '\n'
    
    def mk_csv_header(self):
        return 'TradingDay,Symbol,OpenPrice,ClosePrice,HighestPrice,LowestPrice, \
            Turnover,Volume,LastPrice,AveragePrice,PreClosePrice,UpperLimitPrice,LowerLimitPrice,OpenInterest,PreOpenInterest,PreSettlementPrice, \
            SettlementPrice,AskPrice1,AskPrice2,AskPrice3,AskPrice4,AskPrice5,AskVolume1,AskVolume2,AskVolume3,AskVolume4,AskVolume5,BidPrice1, \
            BidPrice2,BidPrice3,BidPrice4,BidPrice5,BidVolume1,BidVolume2,BidVolume3,BidVolume4,BidVolume5'
    
    def fetch(self):
        return self.data
        
    def is_in_trading(self,day,dt):
        # mk open-close time    
        if self.day != day:
            self.day = day
            self.am_open_dt = datetime.datetime.strptime(day + self.str_am_open,'%Y%m%d%H%M')
            self.am_close_dt = datetime.datetime.strptime(day + self.str_am_close,'%Y%m%d%H%M')
            self.pm_open_dt = datetime.datetime.strptime(day + self.str_pm_open,'%Y%m%d%H%M')
            self.pm_close_dt = datetime.datetime.strptime(day + self.str_pm_close,'%Y%m%d%H%M')
            
        if dt < self.am_open_dt or dt > self.pm_close_dt or (dt > self.am_close_dt and dt < self.pm_open_dt):
            return False
        else:
            return True
