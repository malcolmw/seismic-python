from distutils.core import setup, Extension
import os
import sys
setup(name="response",
      version="1.0",
      ext_modules=[Extension("response",
                             ["responsemodule.c"],
                             include_dirs=['%s/include' % os.environ['ANTELOPE']],
#The set of libraries below is a hack!
#The functions to manipulate response files ($ANTELOPE/html/response.3.html)
#require libraries 'response' and $STOCKLIBS. See $ANTELOPEMAKE for expansion
#of $STOCKLIBS.
                             libraries=['coords',
                                        'alk',
                                        #'banner',
                                        'stock',
                                        'deviants',
                                        'brttpool',
                                        'response'],
                             library_dirs=['%s/lib' % os.environ['ANTELOPE']]
                            )
                  ]
     )
