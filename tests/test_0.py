import pytest
import sys
import pandas
import jupyter

def test_python_installed():
    """Test that Python is available"""
    assert sys.version_info.major >= 3


def test_pandas_installed():
    """Test that pandas is installed"""
    assert hasattr(pandas, 'DataFrame')
