import unittest
import bootstrap

suite = unittest.TestLoader().discover(
    bootstrap.testing_base_path,
    pattern='test_*.py'
)
unittest.TextTestRunner(verbosity=1).run(suite)
