# -*- coding: utf-8 -*-
"""
obspy.datamark - DataMark read support for ObsPy
================================================
This module provides read support for DataMark waveform data.

:copyright:
    The ObsPy Development Team (devs@obspy.org), Thomas Lecocq, Adolfo Inza &
    Philippe Lesage
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)

"""

from obspy.core.util import _getVersionString


__version__ = _getVersionString("obspy.datamark")


if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
