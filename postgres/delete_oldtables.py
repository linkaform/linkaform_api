


import os

linkaform = open('/var/tmp/linkaform.txt.org')
tables = ()
for row in linkaform:
    tables = tables + (row.strip('\n'),)

openerp = open('/var/tmp/openerp_tables.txt')

delete_tables = []

for row in openerp:
    row = row.strip('\n')
    if row in tables:
        if row[-4:] == '_seq':
            delete_tables.append('DROP SEQUENCE %s CASCADE;'%row)
        else:
            delete_tables.append('DROP TABLE %s CASCADE;'%row)

for tt in delete_tables:
    print tt
