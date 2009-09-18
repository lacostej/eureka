cat exo1.txt | python ./exoparse.py

mkdir -p gen
cat data/oppgaver4.txt | python ./mathparse.py > gen/oppgaver4.log 2>&1 

