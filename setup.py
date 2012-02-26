from distutils.core import setup
from sys import exit

try:
    import yotsuba
except:
    print 'Install the package "yotsuba" first.'
    exit(1)

setup(
    name='Imagination',
    version='1.0',
    description='Reusable Component Framework',
    author='Juti Noppornpitak',
    author_email='juti_n@yahoo.co.jp',
    url='http://shiroyuki.com/projects/imagination',
    packages=['imagination']
)