import sys
import unittest

import bootstrap

pattern = len(sys.argv) > 1 and sys.argv[1] or 'test_*.py'

if pattern[:5] != 'test_':
    pattern = 'test_' + pattern

if pattern[-3:] != '.py':
    pattern = pattern + '.py'

suite = unittest.TestLoader().discover(
    bootstrap.testing_base_path,
    pattern=pattern
)

unittest.TextTestRunner(verbosity=1).run(suite)
