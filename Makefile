package:
	python setup.py sdist

clean:
	rm -Rf MANIFEST dist docs/build/*
	find imagination -name *.pyc -exec rm {} \;
