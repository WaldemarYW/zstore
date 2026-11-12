SIZE 30 mm, 20 mm
GAP 3 mm, 0 mm
DIRECTION 0
CLS
TEXT 15,14,"1",0,1,1,"{{name1}}"
TEXT 15,30,"1",0,1,1,"{{name2}}"
{{#isbarcode}}
BARCODE 25,56,"128",42,0,0,3,3,"{{barcode}}"
{{/isbarcode}}
TEXT 75,104,"4",0,1,1,"# {{shop_code}}"
PRINT 1,1
