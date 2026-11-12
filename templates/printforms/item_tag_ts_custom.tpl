SIZE 30 mm, 20 mm
GAP 6.6 mm, 0 mm
DIRECTION 0
CLS
TEXT 15,8,"1",0,1,1,"{{name1}}"
TEXT 15,24,"1",0,1,1,"{{name2}}"
{{#isbarcode}}
BARCODE 45,50,"128",38,0,0,2,2,"{{barcode}}"
{{/isbarcode}}
TEXT 75,94,"4",0,1,1,"# {{shop_code}}"
PRINT 1,1
