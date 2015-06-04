# some examples
tstr = '2015-01-05 09:14:06'
start = as.POSIXct(tstr,tz='GMT')

tstr1 = '2015-01-05 09:16:06'  
end = as.POSIXct(tstr1,tz='GMT')

tstr2 = '2015-01-10 09:16:06'  
end2 = as.POSIXct(tstr2,tz='GMT')

bar <-GetBar('helloyz','TF1506','min',start,end)

ticks <-GetTicks('mmmmx','TF1506',c('High','Low'),start,end2)
