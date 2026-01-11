SIZE 30mm,20mm
CLS   
DIRECTION 1    
REM BOX 3,3,294,194,2
TEXT 30,30,"3",0,3,3,"{{price}}"
TEXT 30,100,"1",0,1,1,"{{article}}"
{{#isbarcode}}
BARCODE 30,120,"128",72,1,0,2,4,"{{barcode}}"
{{/isbarcode}}
PRINT 1,1


