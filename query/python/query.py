import datetime
import pylzma
from bson.code import Code
from bson.son import SON
from pymongo import MongoClient

import cffex_parser
import sh_parser
import compress

import pandas as pd
import io
from StringIO import StringIO

def addtime(strt):
    dt = datetime.datetime.strptime(strt + '000','%Y%m%d%H%M%S%f')
    return dt

class Query():
    def __init__(self,com):
        self.com = com
        self.market_name = com.parser.market
        self.ip = com.parser.ip
        self.port = int(com.parser.port)
        self.client = MongoClient(self.ip,self.port)
        self.db = self.client[self.market_name]        

    def GetBar(self,contract_id,type,start,end=datetime.datetime.now(),limit=10000):
        dct = dict(min ='min',hour = 'hour',day = 'day')
            
        if dct.has_key(type):
            records = list(self.db[dct[type]].find({'InstrumentID':contract_id,'Timestamp':{'$gte':start,'$lt':end}}).limit(limit))

            df = pd.DataFrame(records)       
            if not df.empty:
                return df[['Timestamp','High','Low','Open','Close','Volume','Turnover']]

    def GetHistoricalValue(self,contractId,type,filter,mode,start,end=datetime.datetime.now(),limit=10000):
        dct = dict(min ='min',hour = 'hour',day = 'day')
        mode_dct = dict( 
            Count = "count",
            Maximum = "max",
            Minimum = "min",
            Total = "sum",
            Average = 'avg',
            StandardDeviation = 'std')
            
        if not dct.has_key(type) or not mode_dct.has_key(mode):
            return None
            
        if mode_dct[mode] == 'count':
            c = self.db[dct[type]].count({'InstrumentID':contractId,'Timestamp':{'$gte':start,'$lt':end}})
            return c
        elif mode_dct[mode] == 'max':
            pipeline = [
                {'$match':{'InstrumentID':contractId,'Timestamp':{'$gte':start,'$lt':end}}},
                { '$group':{ '_id':'$InstrumentID', 'Max':{'$max':'$' + filter}}}
                ]
            r = list(self.db[dct[type]].aggregate(pipeline))
            if r:
                return r[0]['Max']
        elif mode_dct[mode] == 'min':
            pipeline = [
                {'$match':{'InstrumentID':contractId,'Timestamp':{'$gte':start,'$lt':end}}},
                { '$group':{ '_id':'$InstrumentID', 'Min':{'$min':'$' + filter}}}
                ]
            r = list(self.db[dct[type]].aggregate(pipeline))
            if r:
                return r[0]['Min']
        elif mode_dct[mode] == 'sum':
            pipeline = [
                {'$match':{'InstrumentID':contractId,'Timestamp':{'$gte':start,'$lt':end}}},
                { '$group':{ '_id':'$InstrumentID', 'Sum':{'$sum':'$' + filter}}}
                ]
            r = list(self.db[dct[type]].aggregate(pipeline))
            if r:
                return r[0]['Sum']
        elif mode_dct[mode] == 'avg':
            pipeline = [
                {'$match':{'InstrumentID':contractId,'Timestamp':{'$gte':start,'$lt':end}}},
                { '$group':{ '_id':'$InstrumentID', 'Avg':{'$avg':'$' + filter}}}
                ]
            r = list(self.db[dct[type]].aggregate(pipeline))
            if r:
                return r[0]['Avg']
        elif mode_dct[mode] == 'std':

            func_str =  "function() {" + \
                "   emit(this.InstrumentID," + \
                "   {" + \
                "       'sum':this." + filter + "," + \
                "       'count':1," + \
                "       'diff':0," + \
                "   })" + \
                "}"
                
            mapper = Code(func_str)
                  
            reducer = Code("function(key, values) {"
                        "var a = values[0]; "
                        "for (var i=1/*!*/; i < values.length; i++){"
                            "var b = values[i];"
                            "var delta = a.sum/a.count - b.sum/b.count;"
                            "var weight = (a.count * b.count)/(a.count + b.count);"
                            "a.diff += b.diff + delta*delta*weight;"
                            "a.sum += b.sum;"
                            "a.count += b.count;"
                        "}"
                        "return a;"
                    "}"
            )
            
            finalizer = Code("function(key,value){"
                        "   var variance = value.diff/value.count;"
                        "   var stddev = Math.sqrt(variance);"
                        "   return stddev;"
                        "}"
            )
            
            results = self.db[dct[type]].map_reduce(mapper,reducer,"results",finalize = finalizer)
            x = results.find({"_id":contractId})
            if x:
                return x[0]['value']
        
    def GetTicks(self,contractId,fields,start,end=datetime.datetime.now(),limit=10000):
        raw = self.db.ticks.find({'InstrumentID':contractId,'Timestamp':{'$gte':start,'$lt':end}}).limit(limit);
        
        s = 'TradingDay,Symbol,OpenPrice,ClosePrice,HighestPrice,LowestPrice, \
            Turnover,Volume,LastPrice,AveragePrice,PreClosePrice,UpperLimitPrice,LowerLimitPrice,OpenInterest,PreOpenInterest,PreSettlementPrice, \
            SettlementPrice,AskPrice1,AskPrice2,AskPrice3,AskPrice4,AskPrice5,AskVolume1,AskVolume2,AskVolume3,AskVolume4,AskVolume5,BidPrice1, \
            BidPrice2,BidPrice3,BidPrice4,BidPrice5,BidVolume1,BidVolume2,BidVolume3,BidVolume4,BidVolume5'
        name = s.split(',')
        
        for var in fields:
            if not var in name:
                return None
        
        records = []
        for binary in raw:
            lzma = binary['Data']
            csv = self.com.uncompress_compatible(lzma)
            x = pd.read_csv(StringIO(csv),names = name, index_col = None,\
                parse_dates =['TradingDay'], header= None,date_parser=addtime)
            records.append(x)
        
        if len(records) > 0:
            df = pd.concat(records)          
            return df[fields]
    
if __name__ == "__main__":

    start = datetime.datetime(2015,1,3,14)
    end = datetime.datetime(2016,4,30,11)
    parser = cffex_parser.CFFEX_Parser('m.conf')
    com = compress.Compress(parser)
       
    q = Query(com)
    x = q.GetBar('TF1506','min',start)

    print x
    #print q.GetHistoricalValue('TF1506','kIntervalType_1min','Close','StandardDeviation',start,end)
    data = q.GetTicks('TF1506',['TradingDay','LastPrice','HighestPrice','LowestPrice'],start,end,1)
    print data 