from distutils.core import setup

setup(
    name         = 'Imagination',
    version      = '1.5.6',
    description  = 'Reusable Component Framework',
    author       = 'Juti Noppornpitak',
    author_email = 'juti_n@yahoo.co.jp',
    url          = 'http://shiroyuki.com/work/projects-imagination',
    packages     = ['imagination', 'imagination.decorator', 'imagination.helper', 'imagination.meta'],
    install_requires = ['kotoba']
)
