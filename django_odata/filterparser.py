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
   #'and': 'AND'
}


# List of token names.
tokens = (
	'NUMBER',
	'EQ',
	'NE',
	'GT',
	'GE',
	'LT',
	'LE',
	'STARTSWITH',
	'AND',
	'OR',
	'LPAREN',
	'RPAREN',
	'ID'
) + tuple(reserved.values())


# Regular expression rules for simple tokens
t_EQ			= 'eq'
t_NE			= r'ne'
t_GT			= r'gt'
t_GE			= r'gt'
t_LT			= r'lt'
t_LE 			= r'le'
t_LPAREN 	= r'\('
t_RPAREN 	= r'\)'
t_ID			= r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ignore = " \t" # ignored characters (spaces and tabs)
t_STARTSWITH = r'startswith'

def t_OR(t):
	'or'
	return {}


def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)    
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
	print(str)


def p_filter(t):
	'filter : constraint'
	debug_print('filter')
	t[0] = t[1]


def p_constraint(t):
	'constraint : ID NUMBER'
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
		parse('teste 1 or test 3')
		#self.assertEqual((1 + 2), 3)
		#self.assertEqual(0 + 1, 1)

if __name__ == '__main__':
	unittest.main()