GetBar <- function(market, contract_id, type, start, end = as.POSIXlt(Sys.time(), "GMT"), limit = 1000) {
  ip <- '127.0.0.1'
  port <- '27017'
  uri <- paste(ip,port,sep=':')
  mongo <- rmongodb::mongo.create(uri)
  fields <- c('Timestamp','InstrumentID','Open','High','Low','Close','Volume','Turnover')
  
  if(rmongodb::mongo.is.connected(mongo) == TRUE) {
    coll = paste(market,type,sep='.') 
    
    #records <- rmongodb::mongo.find(mongo, coll, query = list('InstrumentID'= contract_id,'Timestamp' = list('$gte' = start), 'Timestamp' = list('$lt' = end)),limit = limit)
    #df <- rmongodb::mongo.cursor.to.data.frame(records)
    records <- rmongodb::mongo.find.all(mongo, coll, query = list('InstrumentID'= contract_id,'Timestamp' = list('$gte' = start), 'Timestamp' = list('$lt' = end)),limit = limit)
    df <- do.call("rbind", lapply(records, data.frame))
  }
  
  return (df[fields])
}

GetTicks <- function(market, contract_id,fields,start, end = as.POSIXlt(Sys.time(), "GMT"), limit = 30) {
  ip <- '127.0.0.1'
  port <- '27017'
  uri <- paste(ip,port,sep=':')
  mongo <- rmongodb::mongo.create(uri)
  
  if(rmongodb::mongo.is.connected(mongo) == TRUE) {
    coll = paste(market,'ticks',sep='.')  
    
    records <- rmongodb::mongo.find.all(mongo, coll, query = list('InstrumentID'= contract_id,'Timestamp' = list('$gte' = start), 'Timestamp' = list('$lt' = end)),limit = limit)
    #df <- do.call("rbind", lapply(records, data.frame))
    for (i in 1:length(records))
    {
      t <- records[[i]]$Timestamp
      paste("total number is",str(t))
    }

  }
  
  return (records)
}  