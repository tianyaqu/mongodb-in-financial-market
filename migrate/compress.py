import csv
import datetime
import pylzma
import struct
from cStringIO import StringIO

class Compress():
    def __init__(self,parser):
        self.parser = parser
        self.market_name = self.parser.market

    def filter_file(self,path,file,contract_code):
        day = filter(lambda x:x.isdigit(),file)
                
        content = ''
        with open(path+file) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:                   
                self.parser.parse(row,day,self.market_name)
                dic = self.parser.fetch()
                
                if dic['InstrumentID'] != contract_code:
                    continue                

                strt = day + dic['UpdateTime'] + dic['UpdateMillisec'] + '000'
                dt = datetime.datetime.strptime(strt,'%Y%m%d%H%M%S%f')
                
                if not self.parser.is_in_trading(day,dt):
                    continue
                
                content += self.parser.to_str()
                
        return content
        
    def compress_compatible(self,data):
        c = pylzma.compressfile(StringIO(data))
        # LZMA header
        result = c.read(5)
        # size of uncompressed data
        result += struct.pack('<Q', len(data))
        # compressed data
        return result + c.read()
        
    def uncompress_compatible(self,data):
        datax = data[0:5]+data[13:]
        content = pylzma.decompress(datax)
        return content
              
        
if __name__ == "__main__":
    filename = 'CFFEX_20150403.csv'
    parser = cffex_parser.MyParser('m.conf')
    com = Compress(parser)
    pass