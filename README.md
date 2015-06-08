# mongodb-in-financial-market
mongodb solution for future market data

# what and how
This project comes with a  solution to store and query financial data(stocks,contracts and other similar financial instruments) through Mongodb.
It consists of two parts of work:first,migrate the market data(.csv files) to a Mongodb database and then fetch the data through network.

When the data migrations are done,you'll get three levels of bar data in the database,aka per minute,per hour and per day,also the original ticks data
will be kept in a ticks collection,but we compress that data(one instrument per day) before it is put to the database.It saves disk storage and more importantly,
will reduce the transportation time through the wire,especially when you have a really large dataset after years of years accumulation.

It provides with python,Matlab and R interfaces for users to choose their favourite tools.

# usage

## query
two kinds of query,bar type and tick type,they share a very similar grammar even between different programming languages.
for example,python:

    start = datetime.datetime(2015,1,3,14)
    end = datetime.datetime(2016,4,30,11)
    q = Query(com)
    # query bar
    bar = q.GetBar('TF1506','min',start,end)
    #query ticks
    tick = q.GetTicks('TF1506',['TradingDay','LastPrice','HighestPrice','LowestPrice'],start,end,1)

you will find examples in their separate folders.


## migrate
in the migrate folder,you will see a migrate.py,fill the dir with your own directory,and beaware it's not done yet.You'll have to make your own 
copy of parser to dealing with your files,but it's not much work to worry about.see cffex.py or sh.py to get a better understanding.And last,you
have the conf file written in your flavour accordingly,m.conf and sh.conf are easy examples.

After that,just open a terminal and change to the migrate directory,print 'python migrate.py',you see all is so nice and easy.
