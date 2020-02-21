.SECONDARY:

%.out: phase4.py %.3
	python3 phase4.py $* > $@

%.3: phase3.py %.2
	python3 phase3.py $*

%.2: phase2.py %.1
	python3 phase2.py $*

%.1: phase1.py %.in
	python3 phase1.py $*
