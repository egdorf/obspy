# -*- coding: utf-8 -*-
"""
obspy.seg2 - SEG-2 read support for ObsPy
=========================================

The obspy.seg2 package contains methods in order to read files in the SEG-2
format.

:copyright:
    The ObsPy Development Team (devs@obspy.org)
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)

"""

from obspy.core.util import _getVersionString


__version__ = _getVersionString("obspy.seg2")


if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
