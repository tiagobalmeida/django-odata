# ============================================================
# filterparser.py
#
# (C) Tiago Almeida 2016
#
# This module uses PLY (http://www.dabeaz.com/ply/ply.html)
# and a set of grammar rules to parse odata $filter's value
# ============================================================

import ply.lex as lex
import ply.yacc as yacc
import unittest

# ============================================================
# Lexer rules
# ============================================================
reserved = {
   'and': 'AND',
   'or'	: 'OR',
   'eq'	: 'EQ',
   'ne'	: 'NE',
   'gt'	: 'GT',
   'ge'	: 'GE',
   'lt' : 'LT',
   'le' : 'LE',
   'startswith' : 'STARTSWITH',
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

# ============================================================
# Parser rules
# ============================================================
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
	t[0] = {}


def p_constraint(t):
	'constraint : ID operator value'
	debug_print('p_constraint')
	t[0] = {}


def p_constraint_group(t):
	'constraint : LPAREN constraint RPAREN'
	debug_print('parenthesis')
	t[0] = {}


def p_constraint_binop(t):
	'''constraint : constraint OR constraint
								| constraint AND constraint
	'''
	t[0] = {}



def p_operator(t):
	"""
	operator 	: EQ
						| GT
						| GE
						| LT
						| LE
						| NE
	"""
	t[0] = {}



def p_error(t):
	# TODO 
	print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()

def parse(filter_expression):
	return parser.parse(filter_expression)




# ============================================================
# Unit tests
# ============================================================

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
		parse('test1 gt 6 and ( test2 ne 7 or test3 eq 8 )')
		#self.assertEqual((1 + 2), 3)
		#self.assertEqual(0 + 1, 1)
	
	def test8(self):
		parse('test1 gt test2 and ( test2 ne 7 or test3 eq 8 )')

if __name__ == '__main__':
	unittest.main()