''' Testing bootstrap '''

from os.path import abspath, dirname, join
from sys     import path

app_path          = dirname(abspath(__file__))
testing_base_path = join(app_path, 'testcase')

required_modules = ['Imagination']
base_mod_path    = abspath(join(app_path, '..', '..'))

for required_module in required_modules:
    mod_path = join(base_mod_path, required_module)
    path.append(mod_path)
