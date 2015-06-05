# mongodb-in-financial-market
mongodb solution for future market data

# usage

## query
provided with python,matlab,R query interfaces

### python
comming soon...
### matlab

1. matlab connects to mongodb by using mongo-matlab-driver.
2. each day's ticks data is compressed using lzma.the decompress action is done in c/c++ dll,matlab has to communicate
with the external dll using memory buffer. Dll will take care of the memory malloc and free.
3. unzip the mongo-matlab-driver zip,addpath to the directory,then MongoStart() to enable the mongodb driver
4. compile the decompress.dll with the msvc project,take care of the dependency of lzma(7zSDK)
5. let's go on the unexpected journey...

%query tick records from 20150105 to today,specify fields to 'Timestamp','HighPrice','LowPrice' and 'LastPrice',
also the records limit is 9. FYI,ticks data is compressed with lzma.


start_time = datenum(2015,1,5)

[ret,frame] = GetTicks(dbname,'TF1506',{'Timestamp';'HighPrice';'LowPrice';'LastPrice'},start_time,now,9);


%query bar records from 20150105 to today,bar is minute level.

[Timestamp,Volume,Turnover,High,Low,Open,Close]=GetBar(dbname,'TF1506','min',start_time, now);


### R
under developing...
## migrate
to be continued...
