SIZE 30mm,20mm
CLS   
DIRECTION 1    
REM BOX 3,3,294,194,2
TEXT 35,35,"1",0,1,1,"{{name}}"
TEXT 35,100,"1",0,1,1,"{{article}}"
TEXT 150,100,"1",0,1,1,"{{price}}"
{{#isbarcode}}
BARCODE 35,120,"128",72,1,0,2,4,"{{barcode}}"
{{/isbarcode}}
PRINT 1,1


