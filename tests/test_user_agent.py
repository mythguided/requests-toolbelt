# -*- coding: utf-8 -*-
import unittest
import sys
from mock import patch
from requests_toolbelt.utils import user_agent as ua


class Object(object):
    """
    A simple mock object that can have attributes added to it.
    """
    pass


class TestUserAgent(unittest.TestCase):
    def test_user_agent_provides_package_name(self):
        assert "my-package" in ua.user_agent("my-package", "0.0.1")

    def test_user_agent_provides_package_version(self):
        assert "0.0.1" in ua.user_agent("my-package", "0.0.1")


class TestImplementationString(unittest.TestCase):
    @patch('platform.python_implementation')
    @patch('platform.python_version')
    def test_cpython_implementation(self, mock_version, mock_implementation):
        mock_implementation.return_value = 'CPython'
        mock_version.return_value = '2.7.5'
        assert 'CPython/2.7.5' == ua._implementation_string()

    @patch('platform.python_implementation')
    def test_pypy_implementation_final(self, mock_implementation):
        mock_implementation.return_value = 'PyPy'
        sys.pypy_version_info = Object()
        sys.pypy_version_info.major = 2
        sys.pypy_version_info.minor = 0
        sys.pypy_version_info.micro = 1
        sys.pypy_version_info.releaselevel = 'final'

        assert 'PyPy/2.0.1' == ua._implementation_string()

    @patch('platform.python_implementation')
    def test_pypy_implementation_non_final(self, mock_implementation):
        mock_implementation.return_value = 'PyPy'
        sys.pypy_version_info = Object()
        sys.pypy_version_info.major = 2
        sys.pypy_version_info.minor = 0
        sys.pypy_version_info.micro = 1
        sys.pypy_version_info.releaselevel = 'beta2'

        assert 'PyPy/2.0.1beta2' == ua._implementation_string()

    @patch('platform.python_implementation')
    def test_unknown_implementation(self, mock_implementation):
        mock_implementation.return_value = "Lukasa'sSuperPython"

        assert "Lukasa'sSuperPython/Unknown" == ua._implementation_string()
