import pylzma
import datetime
import csv
from bson.binary import Binary
from pymongo import MongoClient
import ConfigParser
import os

import cffex_parser
import sh_parser
import compress

class Migrate():
    def __init__(self,parser):
        self.day = ""
        self.contract_dict = {}
        self.mapper = {}
        self.parser = parser
        self.market_name = self.parser.market
        self.ip = self.parser.ip
        self.port = int(self.parser.port)
        self.client = MongoClient(self.ip,self.port)
        self.db = self.client[self.market_name]        
        
    def migrate(self,path,filename):
        if self.contract_dict:
            self.contract_dict = {}
            
        self.day = filter(lambda x:x.isdigit(),filename)
        dt = datetime.datetime.strptime(self.day,'%Y%m%d')
        w = dt.strftime('%w')

        # discard saturday and sunday
        if w != 0 and w != 6:
            #must migrate bar then ticks
            self.migrate_bar(path,filename)
            self.migrate_ticks(path,filename)
    
    def migrate_bar(self,path,filename):
        pre_day = datetime.datetime(1970,1,1,0,0,0)
        pre_hour = datetime.datetime(1970,1,1,1,0,0)
        pre_min = datetime.datetime(1970,1,1,2,1,0)	

        with open(path+filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:             
                self.parser.parse(row,self.day,self.market_name)
                dct = self.parser.fetch()
                
                strt = self.day + dct['UpdateTime'] + dct['UpdateMillisec'] + '000'
                dt = datetime.datetime.strptime(strt,'%Y%m%d%H%M%S%f')

                if not self.parser.is_in_trading(self.day,dt):
                    continue             
                
                date = dt.date()
                hour = dt.hour
                minute = dt.minute

                resolution_hour = datetime.time(hour,0)
                resolution_minute = datetime.time(hour,minute)

                resolution_day_dt = datetime.datetime.combine(date,datetime.time(0,0)) 
                resolution_hour_dt = datetime.datetime.combine(date,resolution_hour)
                resolution_minute_dt = datetime.datetime.combine(date,resolution_minute)
                
                if not self.contract_dict.has_key(dct['InstrumentID']):
                    self.contract_dict[dct['InstrumentID']] = {'pre_min':pre_min,'pre_hour':pre_hour,'pre_day':pre_day,'open_min':0,'open_hour':0}
                    
                if resolution_minute_dt != self.contract_dict[dct['InstrumentID']]['pre_min']:
                    self.contract_dict[dct['InstrumentID']]['pre_min'] = resolution_minute_dt
                    self.contract_dict[dct['InstrumentID']]['open_min'] = float(dct['LastPrice'])
                    
                if resolution_hour_dt != self.contract_dict[dct['InstrumentID']]['pre_hour']:
                    self.contract_dict[dct['InstrumentID']]['pre_hour'] = resolution_hour_dt
                    self.contract_dict[dct['InstrumentID']]['open_hour'] = float(dct['LastPrice'])
                
                if resolution_day_dt != self.contract_dict[dct['InstrumentID']]['pre_day']:
                    self.contract_dict[dct['InstrumentID']]['pre_day'] = resolution_day_dt
                    self.contract_dict[dct['InstrumentID']]['open_day'] = float(dct['LastPrice'])
                
                if float(dct['LowestPrice']) <= 0:
                    dct['LowestPrice'] = dct['LastPrice']
                if float(dct['HighestPrice']) <= 0:
                    dct['HighestPrice'] = dct['LastPrice']
                
                self.db.day.update({'Timestamp':resolution_day_dt,'InstrumentID':dct['InstrumentID']},{'$set':{'Open':self.contract_dict[dct['InstrumentID']]['open_day'],'Close':float(dct['LastPrice'])},'$min':{'Low':float(dct['LowestPrice'])},'$max':{'High':float(dct['HighestPrice'])},'$inc': {'Volume':int(dct['Volume']),'Turnover':float(dct['Turnover'])}},upsert=True)
                self.db.hour.update({'Timestamp':resolution_hour_dt,'InstrumentID':dct['InstrumentID']},{'$set':{'Open':self.contract_dict[dct['InstrumentID']]['open_hour'],'Close':float(dct['LastPrice'])},'$min':{'Low':float(dct['LowestPrice'])},'$max':{'High':float(dct['HighestPrice'])},'$inc': {'Volume':int(dct['Volume']),'Turnover':float(dct['Turnover'])}},upsert=True)
                self.db.min.update({'Timestamp':resolution_minute_dt,'InstrumentID':dct['InstrumentID']},{'$set':{'Open':self.contract_dict[dct['InstrumentID']]['open_min'],'Close':float(dct['LastPrice'])},'$min':{'Low':float(dct['LowestPrice'])},'$max':{'High':float(dct['HighestPrice'])},'$inc': {'Volume':int(dct['Volume']),'Turnover':float(dct['Turnover'])}},upsert=True)
            
        print self.contract_dict.keys()

    def migrate_ticks(self,path,filename):
        date_day = datetime.datetime.strptime(self.day,'%Y%m%d')
        com = compress.Compress(self.parser)
        sum1 = 0
        sum2 = 0
        for contract_id in self.contract_dict.keys():
            data = com.filter_file(path,filename,contract_id)
            lzma = com.compress_compatible(data)
            sum1 += len(data)
            sum2 += len(lzma)
            self.db.ticks.update({'Timestamp':date_day,'InstrumentID':contract_id},{'$set':{'Data':Binary(lzma)}},upsert=True)
        print sum1,sum2,sum1*1.0/sum2,'%'

if __name__ == "__main__":

    dir = 'c:\\users\\alex\\desktop\\data\\x\\'
    files = os.listdir(dir)
    #files = ['CFFEX_20150403.csv']
    
    parser = cffex_parser.CFFEX_Parser('m.conf')
    mg = Migrate(parser)

    shparser = sh_parser.SHParser('sh.conf')
    shmg = Migrate(shparser)
    
    for filename in files:
        print 'migrate ' + filename    
        if filename.startswith('CFFEX'):
            mg.migrate(dir,filename)
        elif filename.startswith('SH'):
            shmg.migrate(dir,filename)