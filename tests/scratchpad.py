import django_odata.odata as odata
m = odata.odata_filter_parse('id eq 2')
print( m.group('val') )
print( m.group('op') )
print( m.group('path') )