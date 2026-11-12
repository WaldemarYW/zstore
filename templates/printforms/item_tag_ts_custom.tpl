SIZE 30 mm, 20 mm
GAP 5.3 mm, 0 mm
SHIFT -8
DIRECTION 0
CLS
TEXT 15,0,"1",0,1,1,"{{name1}}"
TEXT 15,16,"1",0,1,1,"{{name2}}"
{{#isbarcode}}
BARCODE 45,36,"128",38,0,0,2,2,"{{barcode}}"
{{/isbarcode}}
TEXT 75,78,"4",0,1,1,"# {{shop_code}}"
PRINT 1,1
