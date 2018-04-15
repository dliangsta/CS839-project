MAIN      = main
SRCS      = *.tex 
TARG      = $(MAIN).pdf

all: $(TARG)

pdf: $(SRCS)
	source ./SourceMe ; \
	pdflatex $(MAIN)
	source ./SourceMe ; \
	pdflatex $(MAIN)
	cp main.pdf ../report.pdf
	
$(TARG): $(SRCS)
	source ./SourceMe ; \
	pdflatex $(MAIN)
	source ./SourceMe ; \
	pdflatex $(MAIN)
	touch $(TARG)
	cp main.pdf ../report.pdf

$(MAIN).aux: $(MAIN).tex
	source ./SourceMe ; \
	pdflatex $(MAIN)

clean:
	rm -f $(TARG) *.aux *~ $(MAIN).log $(MAIN).bbl $(MAIN).blg *.pdf

.SECONDARY: $(DVI)