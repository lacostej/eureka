rm *~
rm *.pyc
rm parser.out
grep "his file is automatically generated. Do not edit" *.py | cut -d ':' -f 1 | xargs rm
