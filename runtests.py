#! /usr/bin/env python
import os
import subprocess
import sys

import pytest

PYTEST_ARGS = {
    'default': ['tests', '--tb=short', '-s', '-rw'],
    'fast': ['tests', '--tb=short', '-q', '-s', '-rw'],
}

#sys.path.append(os.path.dirname(__file__))


def exit_on_failure(ret, message=None):
	if ret:
		sys.exit(ret)


if __name__ == "__main__":
	pytest_args = PYTEST_ARGS['default']
	exit_on_failure(pytest.main(pytest_args))




# import os
# import sys

# import django
# from django.conf import settings
# from django.test.utils import get_runner

# if __name__ == "__main__":
# 	os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
# 	django.setup()
# 	TestRunner = get_runner(settings)
# 	test_runner = TestRunner()
# 	failures = test_runner.run_tests(["tests"])
# 	sys.exit(bool(failures))