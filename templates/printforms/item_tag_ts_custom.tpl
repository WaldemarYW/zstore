SIZE 30 mm, 20 mm
GAP 5.3 mm, 0 mm
DIRECTION 0
CLS
TEXT 15,2,"1",0,1,1,"{{name1}}"
TEXT 15,18,"1",0,1,1,"{{name2}}"
{{#isbarcode}}
BARCODE 45,44,"128",38,0,0,2,2,"{{barcode}}"
{{/isbarcode}}
TEXT 75,88,"4",0,1,1,"# {{shop_code}}"
PRINT 1,1
