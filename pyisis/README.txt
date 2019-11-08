Dependencies
============

  * for the development environment
    - nosetest 0.11.0+ (http://code.google.com/p/python-nose/)
    - figleaf 0.6.1+   (easy_install figleaf)

Generate Documentation API
==========================

  * cd doc/api
  * epydoc --html -o . --graph=all ../../pyisis/pyisis/

Testing
=======

  * cd pyisis/tests
  * run the command:

       nosetests -vv <filename>
