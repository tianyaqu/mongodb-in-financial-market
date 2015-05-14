function [Timestamp,Volume,Turnover,High,Low,Open,Close] = GetBar(db,contract_id,bar_type,start_time,varargin)
    numvarargs = length(varargin);
    optargs(1:numvarargs) = varargin;
    
    switch numvarargs
        case 0
            end_time = now;
            limit = 10000;      
        case 1
            [end_time] = optargs{:};
            limit = 10000;
        case 2
            [end_time, limit] = optargs{:};
        otherwise
            error('parame too much')
    end

    
    if isempty(db) || isempty(contract_id) || isempty(bar_type) || isempty(start_time)
        error('para required not exist')
    end

    collection_name = '';
    switch bar_type
        case 'min'
            collection_name = 'min';
        case 'hour'
            collection_name = 'hour';
        case 'day'
            collection_name = 'day';
        otherwise
            error('time interval not exist')
    end
        
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
    Timestamp = [];
    Volume = [];
    Turnover = [];
    Open = [];
    Close = [];
    High = [];
    Low = [];
    
    x = mongo.find(ns, cursor);
    if x 
        while cursor.next()
            b = cursor.value();
            %datestr(b.value('Timestamp'))     
            Timestamp = [Timestamp;b.value('Timestamp')];
            Volume = [Volume;b.value('Volume')];
            Turnover = [Turnover;b.value('Turnover')];
            Open = [Open;b.value('Open')];
            Close = [Close;b.value('Close')];
            High = [High;b.value('High')];
            Low = [Low;b.value('Low')];
         end
    end