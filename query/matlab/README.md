# query in matlab

query fucntions relys on [mongo-matlab-driver](https://github.com/gerald-lindsly/mongo-matlab-driver) ,as you can see i put the driver in project folder.

# usage
Firstly you need the two steps done before you make the query.

1. unzip the mongo-matlab-driver zip,addpath to the driver directory,then MongoStart() to enable the mongodb driver
2. compile the decompress.dll with the msvc project,take care of the dependency of lzma(7zSDK)

Now let's make the query

    start_time = datenum(2015,1,5)
    [ret,frame] = GetTicks(dbname,'TF1506',{'Timestamp';'HighPrice';'LowPrice';'LastPrice'},start_time,now,9);

    %query bar records from 20150105 to today,bar is minute level.
    [Timestamp,Volume,Turnover,High,Low,Open,Close]=GetBar(dbname,'TF1506','min',start_time, now);