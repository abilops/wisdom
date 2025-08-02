wisdom.pdf: wisdom.tex front.tex pre.tex wisdom.md.tex
	xelatex wisdom.tex

wisdom.md.tex: ../wisdom.md md-to-tex.py
	python md-to-tex.py ../

pre.tex: ../wisdom.md md-to-tex.py
	python md-to-tex.py ../
