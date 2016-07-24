PY            = python3
SPHINXBUILD   = sphinx-build
DOCPREFIX     = docs
BUILDDIR      = $(DOCPREFIX)/build
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(DOCPREFIX)/source
BUILD_PKG_OPT = sdist
RELEASE_OPT   = sdist bdist_wheel upload
LXC_MOUNT_POINT=/opt/src-original
LXC_WORKING_DIR=/opt/src
LXC_TEST_DOCKER_COMMAND=docker run \
	-it --rm \
	-w $(LXC_MOUNT_POINT) \
	-v `pwd`:$(LXC_MOUNT_POINT):ro \
	python
LXC_TEST_EXECUTE=bash -c "make test-lxc-run"

package:
	$(PY) setup.py $(BUILD_PKG_OPT)

release:
	$(PY) setup.py $(RELEASE_OPT)

install:
	$(PY) setup.py install

test-v2:
	$(PY) -m unittest discover -s test/v2

test: clean-cache
	$(PY) -m unittest discover -s test/testcase -t test/
	$(PY) -m unittest discover -s test/v2

test-lxc: clean-cache test-lxc-quick test-lxc-primary
	@(make test-lxc-secondary || echo "\nWARNING: Failed tests on legacy support")

test-lxc-primary:
	@echo "===================================================================="
	@echo "Primary test runs"
	@PY_VERSION=latest make test-lxc-on-version

test-lxc-secondary:
	@echo "===================================================================="
	@echo "Secondary test runs"
	@PY_VERSION=3.4 make test-lxc-on-version
	@PY_VERSION=3.5 make test-lxc-on-version

test-lxc-legacy:
	@echo "===================================================================="
	@echo "Legacy test runs"
	@PY_VERSION=2.7 make test-lxc-on-version
	@PY_VERSION=3.3 make test-lxc-on-version

test-lxc-on-version:
	@echo "--------------------------------------------------------------------"
	@echo "Testing with Python $(PY_VERSION)"
	@echo "--------------------------------------------------------------------"
	@time $(LXC_TEST_DOCKER_COMMAND):$(PY_VERSION) $(LXC_TEST_EXECUTE)
	@echo ""

test-lxc-run:
	@cp -r $(LXC_MOUNT_POINT) $(LXC_WORKING_DIR)
	@pip install -q nose kotoba $(LXC_WORKING_DIR)
	@cd $(LXC_WORKING_DIR) && nosetests -c nose.cfg

doc:
	#cd docs && make clean && make html
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

clean: clean-cache
	rm -Rvf MANIFEST build dist docs/build/* imagination.egg-info; echo 'Cache cleared'

clean-cache:
	find . -name *.pyc -exec rm {} \;
