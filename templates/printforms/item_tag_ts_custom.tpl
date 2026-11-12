SIZE 30 mm, 20 mm
GAP 3 mm, 0 mm
DIRECTION 0
CLS
TEXT 15,20,"1",0,1,1,"{{name1}}"
TEXT 15,36,"1",0,1,1,"{{name2}}"
{{#isbarcode}}
BARCODE 25,65,"128",42,0,0,3,3,"{{barcode}}"
{{/isbarcode}}
TEXT 75,114,"4",0,1,1,"# {{shop_code}}"
PRINT 1,1
