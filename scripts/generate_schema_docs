import sys
import os
import site
sys.path.append('%s/data/python' % os.environ['ANTELOPE'])
site.addsitedir('%s/lib/python' % os.environ['ANF'])
from seispy.core.database import Database
from seispy.util.schema import Schema

for schema in sorted(os.listdir('/home/mcwhite/src/SeismicPython/data/schemas')):
    myschema = Schema(schema=schema)
    myschema.write_sphinx_docs('/home/mcwhite/src/SeismicPython/sphinx-docs/source/schemas')
    print schema, "successfully converted..."
