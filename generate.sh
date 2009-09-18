mkdir -p gen
cat data/oppgaver4.txt | python ./mathparse.py > gen/exos.tex
latex gen/exos.tex

