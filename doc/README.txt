 
Documentation Generation
========================

 cd pyisis
 epydoc  -v -o ../doc/api `ls *.py` tools/pymx.py


Testing
=======

 Using nose (example):

   cd pyisis
   nosetests --with-doctest -w pyisis/ files.py
   nosetests  -w pyisis/tests/ test_mst.py

   cd pyisis/pyisis
   nosetests --with-doctest files.py -v

  
Tutorial
========

Tutorial on how to use the pyisis tools inside an interactive Python session.

# start Python interpreter in interactive mode
$ python

Check the file console_tutorial for examples of valid constructions.

Formatting Language
===================

Some textual formatting is being ignored (not implemented)
because it does not make sense in Web applications.
Either it will remain not supported, or expressions having
textual formatting commands will parse-and-ignore them.
