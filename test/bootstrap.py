''' Testing bootstrap '''

import os
import sys

testing_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testcase')
module_base_path  = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

sys.path.append(module_base_path)