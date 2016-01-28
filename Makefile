SPHINXBUILD   = sphinx-build
DOCPREFIX     = docs
BUILDDIR      = $(DOCPREFIX)/build
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(DOCPREFIX)/source

package:
	python3 setup.py sdist || python setup.py sdist

release:
	python3 setup.py sdist bdist_wheel upload || python setup.py sdist bdist_wheel upload

test: cache_clean
	nosetests -c nose.cfg

doc:
	#cd docs && make clean && make html
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

clean: cache_clean
	rm -Rf MANIFEST build dist docs/build/*

cache_clean:
	find . -name *.pyc -exec rm {} \;
