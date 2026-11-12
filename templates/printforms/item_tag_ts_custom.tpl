SIZE 30 mm, 20 mm
GAP 4.2 mm, 0 mm
DIRECTION 0
CLS
TEXT 15,10,"1",0,1,1,"{{name1}}"
TEXT 15,26,"1",0,1,1,"{{name2}}"
{{#isbarcode}}
BARCODE 45,52,"128",38,0,0,2,2,"{{barcode}}"
{{/isbarcode}}
TEXT 75,96,"4",0,1,1,"# {{shop_code}}"
PRINT 1,1
