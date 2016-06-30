"""The test configuration

.. seealso:: `pytest reference <http://pytest.org/latest/fixture.html>
"""

import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", ".."))
