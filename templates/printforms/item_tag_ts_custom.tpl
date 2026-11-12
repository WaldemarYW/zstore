SIZE 30 mm, 20 mm
GAP 3 mm, 0 mm
DIRECTION 1
CLS
TEXT 15,10,"1",0,1,1,"{{name1}}"
TEXT 15,24,"1",0,1,1,"{{name2}}"
{{#isbarcode}}
BARCODE 25,46,"128",52,0,0,3,3,"{{barcode}}"
{{/isbarcode}}
TEXT 65,112,"3",0,1,1,"# {{shop_code}}"
PRINT 1,1
