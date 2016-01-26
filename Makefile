SPHINXBUILD   = sphinx-build
DOCPREFIX     = docs
BUILDDIR      = $(DOCPREFIX)/build
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(DOCPREFIX)/source

package:
	python setup.py sdist

wheel_release:
	python setup.py sdist bdist_wheel upload

test: cache_clean
	nosetests -c nose.cfg

test_py3:
	nosetests-3.4 -c nose.cfg

install:
	python setup.py install --optimize 2 --compile

doc:
	#cd docs && make clean && make html
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

clean: cache_clean
	rm -Rf MANIFEST build dist docs/build/*

cache_clean:
	find . -name *.pyc -exec rm {} \;
