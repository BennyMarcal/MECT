grammar agl;

program: stat* EOF;

stat:  
        instantiation ';'                                       #statInstantiation
    |   assign ';'                                              #statAssign
    |   action ';'                                              #statAction
    |   viewDef                                                 #statView
    |   figureDef                                               #statFigure
    |   loopDef                                                 #statLoop
    ;

assign:  
        ID '=' dataType                                         #assignExisting
    |   instantiation '=' dataType                              #assignInstantiation 
    ;
            
instantiation:  
        ID ':' ID                                               #instantiationDef
    ;

dataType:
        op=('-' | '+') dataType                                 #dataTypeUnary
    |   '(' dataType ',' dataType ')'                           #dataTypePoint
    |   '(' Number (',' | ':') Number ')'                       #dataTypeVector
    |   Number                                                  #dataTypeRealNumber
    |   String                                                  #dataTypeString
    |   action                                                  #dataTypeAction
    |   ID                                                      #dataTypeID
    |   Integer                                                 #dataTypeInteger
    ;

action:
        'close' ID                                              #actionClose
    |   'refresh' ID ('after' Integer ( 'ms' | 's' ))?          #actionRefresh
    |   'print' (String | ID)+                                  #actionPrint
    |   'wait mouse click'                                      #actionMouse
    ;

figureDef:
        (ID | instantiation) 'at' dataPoint 'with' '{' (assign ';')* '}'   #figureDefinition
    ;

viewDef:
        instantiation 'with' '{' (assign ';')* '}'              #viewDefinition
    ;

loopDef:
        'for' ID 'in' Integer '..' Integer ( '..' Integer )? 'do' '{' stat* '}' #loopDefinition
    ;

dataPoint:
        '(' dataType ',' dataType ')'                           #dataPointDef
    ;

ID: [a-zA-Z_][a-zA-Z0-9_]*;

Number: Integer ('.' Integer)?;

Integer: [0-9]+;

String: '"' .*? '"' ;

WS: [ \t\r\n] -> skip;

COMMENT: '#' .*? '\r'?'\n' -> skip;

MULTICOMMENT: '#(' .*? '#)' -> skip;

ERROR: . ;
