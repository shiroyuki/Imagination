SPHINXBUILD   = sphinx-build
DOCPREFIX     = docs
BUILDDIR      = $(DOCPREFIX)/build
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(DOCPREFIX)/source
BUILD_PKG_OPT = sdist
RELEASE_OPT   = sdist bdist_wheel upload
LXC_MOUNT_POINT=/opt/src-original
LXC_WORKING_DIR=/opt/src
LXC_TEST_DOCKER_COMMAND=docker run -i -t --rm -v `pwd`:$(LXC_MOUNT_POINT) python:
LXC_TEST_EXECUTE=bash -c 'cp -r $(LXC_MOUNT_POINT) $(LXC_WORKING_DIR); pip install nosetests kotoba $(LXC_WORKING_DIR) && cd $(LXC_WORKING_DIR) && nosetests -c nose.cfg'

package:
	python3 setup.py $(BUILD_PKG_OPT)

release:
	python3 setup.py $(RELEASE_OPT)

install:
	python3 setup.py install

test: cache_clean
	nosetests -c nose.cfg

test-lxc: cache_clean
	$(LXC_TEST_DOCKER_COMMAND)2.7 "$(LXC_TEST_EXECUTE)"
	$(LXC_TEST_DOCKER_COMMAND)3.3 "$(LXC_TEST_EXECUTE)"
	$(LXC_TEST_DOCKER_COMMAND)3.4 "$(LXC_TEST_EXECUTE)"
	$(LXC_TEST_DOCKER_COMMAND)latest "$(LXC_TEST_EXECUTE)"

doc:
	#cd docs && make clean && make html
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

clean: cache_clean
	rm -Rvf MANIFEST build dist docs/build/* imagination.egg-info; echo 'Cache cleared'

cache_clean:
	find . -name *.pyc -exec rm {} \;
