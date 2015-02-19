try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name         = 'imagination',
    version      = '1.8.2',
    description  = 'Reusable Component Framework',
    author       = 'Juti Noppornpitak',
    author_email = 'juti_n@yahoo.co.jp',
    url          = 'http://shiroyuki.com/work/projects-imagination',
    packages     = ['imagination', 'imagination.decorator', 'imagination.helper', 'imagination.meta']
)
