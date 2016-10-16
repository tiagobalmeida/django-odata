# ============================================================
# Tests for odata module
#
# (C) Tiago Almeida 2016
#
# 
#
# ============================================================
import unittest
import .odata as odata

class TestModels(unittest.TestCase):
	def test_tests(self):
		self.assertEqual(True, True)

	def test_orderby_simple(self):
		"""
		Test parameter $order_by with one property
		"""
		
		odata.set_order_by()

if __name__ == '__main__':
	unittest.main()