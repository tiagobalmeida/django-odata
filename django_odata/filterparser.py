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

# ============================================================
# Lexer rules
# ============================================================
reserved = {}


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
t_EQ			= r'eq'
t_NE			= r'ne'
t_GT			= r'gt'
t_GE			= r'gt'
t_LT			= r'lt'
t_LE 			= r'le'
t_AND 		= r'and'
t_OR 			= r'or'
t_LPAREN 	= r'\('
t_RPAREN 	= r'\)'
t_ID			= r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ignore 	= ' \t' # ignored characters (spaces and tabs)
t_STARTSWITH = r'startswith'


def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)    
	return t


# ============================================================
# Parser rules
# ============================================================
def p_filter_def(t):
	'''filter : constraint
						| constraint OR constraint
						| constraint AND constraint
	'''
	pass


def p_constraint(t):
	'constraint : ID OPERATOR VALUE'
	pass


def p_constraint_group(t):
	'constraint : LPAREN constraint RPAREN'
	pass