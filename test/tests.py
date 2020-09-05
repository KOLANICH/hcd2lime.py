#!/usr/bin/env python3
import typing
import itertools
import os
import sys
import unittest
from pathlib import Path
from random import _urandom, randint

from lime import *

sys.path.insert(0, str(Path(__file__).absolute().parent.parent))

#from collections import OrderedDict
#dict = OrderedDict


def genRandRecord(minAddr=0, minSize=10, maxSize=20, maxAddr=(1 << 64)):
	start = randint(minAddr, maxAddr)
	stop = randint(start + minSize, min(start + maxSize, maxAddr))
	len = stop - start
	payload = _urandom(len)
	return (start, payload)


def genRandDump():
	testStruct = [(0, b"")]
	for i in range(10):
		testStruct.append(genRandRecord(testStruct[-1][0] + len(testStruct[-1][1])))
	del testStruct[0]
	return testStruct


class Tests(unittest.TestCase):
	def test_roundtrip(self):
		d = genRandDump()
		f = dumps(d)
		d1 = loads(f)
		self.assertEqual(d, d1)


if __name__ == "__main__":
	unittest.main()
