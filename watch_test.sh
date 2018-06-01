#/bin/sh
find . *.py | /home/utils/entr-4.0/bin/entr -s "clear && python -m unittest discover -s . -p 'TEST_*.py'"
