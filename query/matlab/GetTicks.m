function [ret,result] = GetTicks(db,contract_id,var_list,start_time,varargin)
    numvarargs = length(varargin);
    optargs(1:numvarargs) = varargin;
    
    switch numvarargs
        case 0
            end_time = now;
            limit = 1;      
        case 1
            [end_time] = optargs{:};
            limit = 10000;
        case 2
            [end_time, limit] = optargs{:};
        otherwise
            error('para too much')
    end
    
    
    
    if isempty(db) || isempty(contract_id) || isempty(start_time) || isempty(var_list)
        error('para required not exist')
    end
    
    var_len = length(var_list);
    if var_len < 1
        error('at least specify one variable')
    end
   
    if ~libisloaded('decompress')
        [notfound, warnings] = loadlibrary('decompress','decompress.h');
    end


    collection_name = 'ticks';
        
    ns = sprintf('%s.%s', db,collection_name);  % Construct a namespace string    
  
    mongo = Mongo();
    
    bb = BsonBuffer;
    %document
    bb.startObject('$query');
    
    %query criteria 1
    bb.append('InstrumentID',contract_id);
    
    %query criteria 2
    bb.startObject('Timestamp');
    bb.appendDate('$gte', start_time);
    bb.appendDate('$lt', end_time);
    bb.finishObject;

    bb.finishObject;
    
    query = bb.finish();
    cursor = MongoCursor(query);
    cursor.limit = limit;

    %prepare result
    result = [];
    Timestamp = [];
    Volume = [];
    Turnover = [];
    OpenPrice = [];
    ClosePrice = [];
    HighPrice = [];
    LowPrice = [];   
    LastPrice = [];
    AveragePrice = [];
    PreClosePrice = [];
    AskPrice1 = [];
    AskPrice2 = [];
    AskPrice3 = [];
    AskPrice4 = [];
    AskPrice5 = [];
    AskVolume1 = [];
    AskVolume2 = [];
    AskVolume3 = [];
    AskVolume4 = [];
    AskVolume5 = [];
    BidPrice1 = [];
    BidPrice2 = [];
    BidPrice3 = [];
    BidPrice4 = [];
    BidPrice5 = [];
    BidVolume1 = [];
    BidVolume2 = [];
    BidVolume3 = [];
    BidVolume4 = [];
    BidVolume5 = [];
    UpperLimitPrice = [];
    LowerLimitPrice = [];
    OpenInterest = [];
    PreOpenInterest = [];
    PreSettlementPrice = [];
    SettlementPrice = [];
    Day = [];
    Update = [];
    Mill = [];

    
    x = mongo.find(ns, cursor);
    if x 
        while cursor.next() 
            b = cursor.value();
            %datestr(b.value('Timestamp'));
            b.value('InstrumentID');
            dx = b.value('Data');

            compress_ptr = libpointer('uint8Ptr',dx);
            tickdDta_ptr = libpointer('TickData');
            len = libpointer('uint32Ptr',0);
            ret = calllib('decompress','decompress',db,compress_ptr,tickdDta_ptr,len);
            if ret == 0
                for i = 1:len.Value
                    offset = i-1;
                    ptr = get(tickdDta_ptr + offset);
                    day = ptr.Value.ActionDay;
                    updatetime = ptr.Value.UpdateTime;
                    mill = ptr.Value.UpdateMillisec;
                    Day = [Day;day];
                    Update = [Update;updatetime];
                    Mill = [Mill;mill];

                    high = ptr.Value.HighestPrice;
                    low = ptr.Value.LowestPrice;
                    last  = ptr.Value.LastPrice;
                    
                    volume = ptr.Value.Volume;
                    turnover = ptr.Value.Turnover;
                    open = ptr.Value.OpenPrice;
                    close = ptr.Value.ClosePrice;
                    ava = ptr.Value.AveragePrice;
                    preclose = ptr.Value.PreClosePrice;
                    askp1 = ptr.Value.AskPrice1;
                    askp2 = ptr.Value.AskPrice2;
                    askp3 = ptr.Value.AskPrice3;
                    askp4 = ptr.Value.AskPrice4;
                    askp5 = ptr.Value.AskPrice5;
            
                    askv1 = ptr.Value.AskVolume1;
                    askv2 = ptr.Value.AskVolume2;
                    askv3 = ptr.Value.AskVolume3;
                    askv4 = ptr.Value.AskVolume4;
                    askv5 = ptr.Value.AskVolume5;
                    
                    bidp1 = ptr.Value.BidPrice1;
                    bidp2 = ptr.Value.BidPrice2;
                    bidp3 = ptr.Value.BidPrice3;
                    bidp4 = ptr.Value.BidPrice4;
                    bidp5 = ptr.Value.BidPrice5;

                    bidv1 = ptr.Value.BidVolume1;
                    bidv2 = ptr.Value.BidVolume2;
                    bidv3 = ptr.Value.BidVolume3;
                    bidv4 = ptr.Value.BidVolume4;
                    bidv5 = ptr.Value.BidVolume5;
            
                    upper = ptr.Value.UpperLimitPrice;
                    lower = ptr.Value.LowerLimitPrice;
                    oprninterest = ptr.Value.OpenInterest;
                    preopeninterest = ptr.Value.PreOpenInterest;
                    presettle = ptr.Value.PreSettlementPrice;
                    settle = ptr.Value.SettlementPrice;
 
                    HighPrice = [HighPrice;high];
                    LowPrice = [LowPrice;low];
                    LastPrice = [LastPrice;last];
            
                    Volume = [Volume;volume];
                    Turnover = [Turnover;turnover];
                    OpenPrice = [OpenPrice;open];
                    ClosePrice = [ClosePrice;close];
                    AveragePrice = [AveragePrice;ava];
                    PreClosePrice = [PreClosePrice;preclose];
                    AskPrice1 = [AskPrice1;askp1];
                    AskPrice2 = [AskPrice2;askp2];
                    AskPrice3 = [AskPrice3;askp3];
                    AskPrice4 = [AskPrice4;askp4];
                    AskPrice5 = [AskPrice5;askp5];
                    AskVolume1 = [AskVolume1;askv1];
                    AskVolume2 = [AskVolume2;askv2];
                    AskVolume3 = [AskVolume3;askv3];
                    AskVolume4 = [AskVolume4;askv4];
                    AskVolume5 = [AskVolume5;askv5];
            
                    BidPrice1 = [BidPrice1;bidp1];
                    BidPrice2 = [BidPrice2;bidp2];
                    BidPrice3 = [BidPrice3;bidp3];
                    BidPrice4 = [BidPrice4;bidp4];
                    BidPrice5 = [BidPrice5;bidp5];
                    BidVolume1 = [BidVolume1;bidv1];
                    BidVolume2 = [BidVolume2;bidv2];
                    BidVolume3 = [BidVolume3;bidv3];
                    BidVolume4 = [BidVolume4;bidv4];
                    BidVolume5 = [BidVolume5;bidv5];
                    
                    UpperLimitPrice = [UpperLimitPrice;upper];
                    LowerLimitPrice = [LowerLimitPrice;lower];
                    OpenInterest = [OpenInterest;oprninterest];
                    PreOpenInterest = [PreOpenInterest;preopeninterest];
                    PreSettlementPrice = [PreSettlementPrice;presettle];
                    SettlementPrice = [SettlementPrice;settle];
                end
    


            end
            
        end
        year = fix(Day/10000);
        t_tmp = rem(Day,10000);
        month = fix(t_tmp/100);
        day = rem(t_tmp,100);
        hour = fix(Update/10000);
        t_tmp1 = rem(Update,10000);
        minute = fix(t_tmp1/100);
        sec = rem(t_tmp1,100);
        Timestamp = datenum(year,month,day,hour,minute,sec) + Mill/(1000*60*60*24);

        char_list = char(var_list);
        try
            for i = 1:var_len
                result = [result eval(char_list(i,:))];
            end
        catch
            ;
        end
    end
    
    calllib('decompress','free_mem',tickdDta_ptr)
    clear tickdDta_ptr;
    if ~libisloaded('decompress')
        unloadlibrary('decompress');
    end