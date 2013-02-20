SPHINXBUILD   = sphinx-build
DOCPREFIX     = docs
BUILDDIR      = $(DOCPREFIX)/build
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(DOCPREFIX)/source

package:
	python setup.py sdist

ut:
	cd test && python test.py
	cd test && python3 test.py

doc:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

clean:
	rm -Rf MANIFEST dist docs/build/*
	find imagination -name *.pyc -exec rm {} \;
