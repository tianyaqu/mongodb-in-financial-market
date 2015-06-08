library(decompress)
library(xts)

#' Get bar data from db
#' 
#' @param market your db's name.
#' @param instrument_id your instrument name.
#' @param type bar types,we provided three types,aka 'min','hour' and 'day'.
#' @param start data from that time.
#' @param end data before that time,default is now.
#' @param limit data number limit,default is 1000.
#' @return data wrapped in xts format.
#' @examples
#' tstr = '2015-01-05 09:14:06'
#' start = as.POSIXct(tstr,tz='GMT')
#' tstr1 = '2015-01-06 10:00:06'
#' end = as.POSIXct(tstr1,tz='GMT')
#' bar <-GetBar('helloyz','TF1506','min',start,end)

GetBar <- function(market, instrument_id, type, start, end = as.POSIXlt(Sys.time(), "GMT"), limit = 1000) {
    ip <- '127.0.0.1'
    port <- '27017'
    uri <- paste(ip,port,sep=':')
    mongo <- rmongodb::mongo.create(uri)
    fields <- c('Timestamp','Open','High','Low','Close','Volume','Turnover')
  
    if(rmongodb::mongo.is.connected(mongo) == TRUE) {
        coll = paste(market,type,sep='.')
        records <- rmongodb::mongo.find.all(mongo, coll, query = list('InstrumentID'= instrument_id,'Timestamp' = list('$gte' = start), 'Timestamp' = list('$lt' = end)),limit = limit)
        df <- do.call("rbind", lapply(records, data.frame))
    }
    
    if(length(df) <= 0)
    {
        return (data.frame())
    }
    
    data <- df[fields]
    df_xts <- xts(data[,-1],order.by=as.POSIXct(df$Timestamp))
    return (df_xts)
}

#' Get ticks data from db
#' 
#' @param market your db's name.
#' @param instrument_id your instrument name.
#' @param field avaiable data fields,'Open','Close','High','Low','Volume','Turnover',
#' 'Last','Average','Preclose','Openinterest','Preopeninterest','Presettle','Settle','Upper','Lower',
#' 'Askprice1','Askprice2','Askprice3','Askprice4','Askprice5',
#' 'Askvolume1','Askvolume2','Askvolume3','Askvolume4','Askvolume5'
#' 'Bidprice1','Bidprice2','Bidprice3','Bidprice4','Bidprice5',
#' 'Bidvolume1','Bidvolume2','Bidvolume3','Bidvolume4','Bidvolume5'.
#' If this filed is null,c(),it will give lastprice,askprice,bidprice and ohlc of day.
#' @param start data from that time.
#' @param end data before that time,default is now.
#' @param limit day number limit,default is 30.
#' @return data wrapped in xts format.
#' @examples
#' tstr = '2015-01-05 00:00:00'
#' start = as.POSIXct(tstr,tz='GMT')
#' tstr1 = '2015-01-08 00:00:00'
#' end = as.POSIXct(tstr1,tz='GMT')
#' ticks <-GetTicks('helloyz','TF1506','min',start,end)
GetTicks <- function(market, instrument_id,fields,start, end = as.POSIXlt(Sys.time(), "GMT"), limit = 30) {
    ip <- '127.0.0.1'
    port <- '27017'
    uri <- paste(ip,port,sep=':')
    mongo <- rmongodb::mongo.create(uri)

    if(rmongodb::mongo.is.connected(mongo) == TRUE) {
        coll = paste(market,'ticks',sep='.')  

        records <- rmongodb::mongo.find.all(mongo, coll, query = list('InstrumentID'= instrument_id,'Timestamp' = list('$gte' = start), 'Timestamp' = list('$lt' = end)),limit = limit)
        len <- length(records)
        
        data_set <- data.frame()
        if(len <= 0)
        {
            return (data_set)  
        }
    
        for (i in 1:length(records))
        {
            t <- records[[i]]$Timestamp
            raw <- records[[i]]$Data
            df = R_decompress(market,raw)
            year <- df[,'day']%/%10000
            t_tmp <- df[,'day']%%10000
            month <- t_tmp%/%100
            day <- t_tmp%%100

            hour <- df[,'updatetime']%/%10000
            t_tmp1 <- df[,'updatetime']%%10000
            minute <- t_tmp1%/%100
            sec <- t_tmp1%%100
            millisec <- df[,'millsec']/1000

            ts <- ISOdatetime(year,month,day,hour,minute,sec,tz="GMT") + millisec
            df$Timestamp <- ts
            
            #delete character columns
            df$id <- NULL
            

            if(length(fields) <= 0)
            {
                data <- df[c('Timestamp','Last','Askprice1','Bidprice1','Open','High','Low','Close')]
                data_set <- rbind(data_set, data)
            }
            else
            {
                data <- df[c('Timestamp',fields)]
                data_set <- rbind(data_set, data)
            }
        }
    
        df_xts <- xts(data_set[,-1],order.by=as.POSIXct(data_set$Timestamp))
        return (df_xts)
    }
}