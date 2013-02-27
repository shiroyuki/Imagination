SPHINXBUILD   = sphinx-build
DOCPREFIX     = docs
BUILDDIR      = $(DOCPREFIX)/build
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(DOCPREFIX)/source

package:
	python setup.py sdist

test: clean
	nosetests -c nose.cfg
	nosetests-3.3 -c nose.cfg

doc:
	#cd docs && make clean && make html
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

clean:
	rm -Rf MANIFEST dist docs/build/*
	find imagination -name *.pyc -exec rm {} \;
