from distutils.core import setup

setup(
    name         = 'imagination',
    version      = '3.0.0a1',
    description  = 'Reusable Component Framework',
    author       = 'Juti Noppornpitak',
    author_email = 'juti_n@yahoo.co.jp',
    url          = 'https://github.com/shiroyuki/Imagination',
    packages     = [
        'imagination',
        'imagination.assembler',
        'imagination.decorator',
        'imagination.helper',
        'imagination.meta',
    ]
)
