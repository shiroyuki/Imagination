PY            = python3
SPHINXBUILD   = sphinx-build
DOCPREFIX     = docs
BUILDDIR      = $(DOCPREFIX)/build
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(DOCPREFIX)/source

package: clean-dist
	python3 -m build

clean-dist:
	@git clean -fdX
	@rm dist/* 2> /dev/null || echo '(/dist is clean...)'

release: package
	@twine upload dist/*

install:
	$(PY) setup.py install

test-local:
	$(PY) -m unittest discover -v test

doc:
	#cd docs && make clean && make html
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

clean: clean-cache
	rm -Rvf MANIFEST build dist docs/build/* imagination.egg-info; echo 'Cache cleared'

clean-cache:
	@find . -name *.pyc -exec rm {} \;
