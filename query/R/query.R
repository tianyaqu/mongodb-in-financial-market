library(decompress)
library(xts)

GetBar <- function(market, contract_id, type, start, end = as.POSIXlt(Sys.time(), "GMT"), limit = 1000) {
  ip <- '127.0.0.1'
  port <- '27017'
  uri <- paste(ip,port,sep=':')
  mongo <- rmongodb::mongo.create(uri)
  fields <- c('Timestamp','Open','High','Low','Close','Volume','Turnover')
  
  if(rmongodb::mongo.is.connected(mongo) == TRUE) {
    coll = paste(market,type,sep='.') 
    
    records <- rmongodb::mongo.find.all(mongo, coll, query = list('InstrumentID'= contract_id,'Timestamp' = list('$gte' = start), 'Timestamp' = list('$lt' = end)),limit = limit)
    df <- do.call("rbind", lapply(records, data.frame))
  }
  data <- df[fields]
  df_xts <- xts(data[,-1],order.by=as.POSIXct(df$Timestamp))
  return (df_xts)
}

GetTicks <- function(market, contract_id,fields,start, end = as.POSIXlt(Sys.time(), "GMT"), limit = 30) {
    ip <- '127.0.0.1'
    port <- '27017'
    uri <- paste(ip,port,sep=':')
    mongo <- rmongodb::mongo.create(uri)

    if(rmongodb::mongo.is.connected(mongo) == TRUE) {
    coll = paste(market,'ticks',sep='.')  

    records <- rmongodb::mongo.find.all(mongo, coll, query = list('InstrumentID'= contract_id,'Timestamp' = list('$gte' = start), 'Timestamp' = list('$lt' = end)),limit = limit)
    len <- length(records)
    
    data_set <- data.frame(Date=as.Date(character()),
                     File=character(), 
                     User=character(), 
                     stringsAsFactors=FALSE)
    
    for (i in 1:length(records))
    {
        t <- records[[i]]$Timestamp
        paste("total number is",str(t))
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

        ts <- ISOdatetime(year,month,day,hour,minute,sec,tz="GMT")+millisec
        df$Timestamp <- ts
        
        #delete character columns
        df$id <- NULL
        

        if(length(fields) <= 0)
            return (df)
        else
            data <- df[c('Timestamp',fields)]
            data_set <- rbind(data_set, data)
     
    }
    
    df_xts <- xts(data_set[,-1],order.by=as.POSIXct(data_set$Timestamp))
    return (df_xts)
  }
}