"""The test configuration used by all tests in this directory.

.. seealso:: `pytest reference <http://pytest.org/latest/fixture.html>
"""

import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
