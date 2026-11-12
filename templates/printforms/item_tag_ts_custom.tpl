SIZE 30 mm, 20 mm
GAP 5.8 mm, 0 mm
DIRECTION 0
CLS
TEXT 15,14,"1",0,1,1,"{{name1}}"
TEXT 15,30,"1",0,1,1,"{{name2}}"
{{#isbarcode}}
BARCODE 45,56,"128",38,0,0,2,2,"{{barcode}}"
{{/isbarcode}}
TEXT 75,100,"4",0,1,1,"# {{shop_code}}"
PRINT 1,1
