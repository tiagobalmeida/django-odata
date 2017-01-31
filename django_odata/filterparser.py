# ===================================================================
# filterparser.py
#
# (C) Tiago Almeida 2016
#
# This module uses PLY (http://www.dabeaz.com/ply/ply.html)
# and a set of grammar rules to parse odata $filter's value.
# The main function is called parse and it returns a
# tree. Every node on the tree is either a Constraint or a 
# BinaryOperator. These are defined below. The Constraint is a simple
# definition for the value of a property, e.g. 'property eq 2', the 
# BinaryOperator can group 2 constraints with a boolean operator.
# If you execute this module from the command line, it will run a 
# set of unit tests.
# 
# TODO:
# IDs can take slashes ( / ) as subobject paths.
# 
# ===================================================================

import ply.lex as lex
import ply.yacc as yacc
import unittest

C_OPERATOR_AND 	= 'AND'
C_OPERATOR_OR 	= 'OR'
C_OPERATOR_GT 	= 'GT'
C_OPERATOR_GE 	= 'GE'
C_OPERATOR_LE 	= 'LE'
C_OPERATOR_LT 	= 'LT'
C_OPERATOR_EQ 	= 'EQ'
C_OPERATOR_NE 	= 'NE'

# ===================================================================
# Abstract syntax tree classes (the output of the parser below)
# ===================================================================
class Constraint:
	"""
	Represents a constraint for the filter. Like property eq 2
	"""
	def __init__(self, sProperty, sOperator, sValue):
		self.property = sProperty
		self.operator = sOperator
		self.value = sValue

class BinaryOperator:
	"""
	Represents a boolean operation on two Constraints or BinaryOperator 
	"""
	def __init__(self, sBooleanOperator, left, right):
		self.operator = sBooleanOperator
		self.left = left
		self.right = right


# ===================================================================
# Lexer rules
# ===================================================================
reserved = {
   'and': C_OPERATOR_AND,
   'or'	: C_OPERATOR_OR,
   'eq'	: C_OPERATOR_EQ,
   'ne'	: C_OPERATOR_NE,
   'gt'	: C_OPERATOR_GT,
   'ge'	: C_OPERATOR_GE,
   'lt' : C_OPERATOR_LT,
   'le' : C_OPERATOR_LE,
   'startswith' : 'STARTSWITH', #TODO
}


# List of token names.
tokens = (
	'NUMBER',
	'LPAREN',
	'RPAREN',
	'ID'
) + tuple(reserved.values())


# Regular expression rules for simple tokens
t_LPAREN 	= r'\('
t_RPAREN 	= r'\)'
t_ignore = " \t" # ignored characters (spaces and tabs)


def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)    
	return t


def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'ID')
	return t 


def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()

# ===================================================================
# Parser rules
# ===================================================================
precedence = (
	('left','OR'),
	('left','AND')
)


def debug_print(str):
	return None
	print(str)


def p_filter(t):
	'filter : constraint'
	debug_print('filter')
	t[0] = t[1]


def p_value(t):
	"""value 	: NUMBER 
						| ID
	"""
	t[0] = t[1]


def p_constraint(t):
	'constraint : ID operator value'
	debug_print('p_constraint')
	t[0] = Constraint(t[1], t[2], t[3])


def p_constraint_group(t):
	'constraint : LPAREN constraint RPAREN'
	debug_print('parenthesis')
	t[0] = t[2]


def p_constraint_binop(t):
	'''constraint : constraint OR constraint
								| constraint AND constraint
	'''
	t[0] = BinaryOperator(reserved.get(t[2]), t[1], t[3])


def p_operator(t):
	"""
	operator 	: EQ
						| GT
						| GE
						| LT
						| LE
						| NE
	"""
	t[0] = reserved.get(t[1])



def p_error(t):
	# TODO 
	print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()

def parse(filter_expression):
	return parser.parse(filter_expression)




# ===================================================================
# Unit tests
# ===================================================================

class TestCase(unittest.TestCase):
	def test1(self):
		parse('test eq 1 or test eq 3')
	
	def test2(self):	
		parse('test ne 2')
	
	def test3(self):
		parse('test lt 3')
	
	def test4(self):
		parse('test le 4')
	
	def test5(self):
		parse('test ge 5')
	
	def test6(self):
		parse('test gt 6')
	
	def test7(self):
		"""
		Tests a more complex input and makes sure the parsed tree looks
		correct.
		"""
		tree = parse('test1 gt 6 and ( test2 ne 7 or test3 eq 8 )')
		# We should have, a BinOp with test1>6 and the rest.
		# The rest should be a BinOp with test2!=7 | test3=8
		# Let's test for this.
		self.assertTrue(isinstance(tree, BinaryOperator))
		self.assertEqual(tree.operator, C_OPERATOR_AND)
		self.assertTrue(isinstance(tree.left, Constraint))
		self.assertFalse(isinstance(tree.right, Constraint))
		left = tree.left
		right = tree.right
		self.assertEqual(left.operator, C_OPERATOR_GT)
		self.assertEqual(left.property, 'test1')
		self.assertEqual(left.value, 6)
		self.assertEqual(right.operator, C_OPERATOR_OR)
		# rightmost part of the expression
		left = right.left
		right = right.right
		self.assertEqual(left.property, 'test2')
		self.assertEqual(right.property, 'test3')
		self.assertEqual(left.operator, C_OPERATOR_NE)
		self.assertEqual(right.operator, C_OPERATOR_EQ)
		self.assertEqual(left.value, 7)
		self.assertEqual(right.value, 8)

	
	def test8(self):
		parse('test1 gt test2 and ( test2 ne 7 or test3 eq 8 )')


	def test9(self):
		"""
		Tests precedence - Should group the and together
		"""
		tree = parse('test1 eq 1 and test2 eq 2 or test3 eq 3')
		self.assertEqual(tree.operator, C_OPERATOR_OR)
		self.assertEqual(tree.left.operator, C_OPERATOR_AND)


	def test10(self):
		"""
		Tests precedence. Should group the and together
		"""
		tree = parse('t1 eq 1 or t2 eq 2 or t3 eq 3 and t4 eq 4')
		self.assertEqual(tree.operator, C_OPERATOR_OR)
		self.assertEqual(tree.right.operator, C_OPERATOR_AND)
		self.assertEqual(tree.left.operator, C_OPERATOR_OR)
		self.assertEqual(tree.left.left.value, 1)
		self.assertEqual(tree.left.right.value, 2)
		self.assertEqual(tree.right.left.value, 3)
		self.assertEqual(tree.right.right.value, 4)


	def test11(self):
		"""
		Tests precedence. Should group the and together
		"""
		tree = parse('t1 eq 1 or t2 eq 2 and t3 eq 3 or t4 eq 4')
		# equivalent '(t1 eq 1 or (t2 eq 2 and t3 eq 3)) or t4 eq 4'
		self.assertEqual(tree.right.value, 4)
		self.assertEqual(tree.right.operator, C_OPERATOR_EQ)
		tree = tree.left
		self.assertEqual(tree.operator, C_OPERATOR_OR)
		self.assertEqual(tree.right.operator, C_OPERATOR_AND)
		self.assertTrue(isinstance(tree.left, Constraint))
		

if __name__ == '__main__':
	unittest.main()