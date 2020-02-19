INCREMENT, DECREMENT, DOUBLESLASH, END, NLANGSTART, NLANGEND, STATIC, PRIVATE, PROTECTED, PUBLIC, VOID, HEX_NUMBER, NUM, STRING, CUSTOM, VARIABLE, NONE, ARRAY, LIST, DICT, IF, ELSE, WHILE, FOR, BREAK, CONTINUE, RETURN, CASE, FUNCTION, CLASS, SYSTEM_FUNCTION, AUTO, BOOL, NEW, DOLLAR, PLUS, MINUS, STAR, SLASH, PERCENT, AT, EQUAL, EQEQ, EXCL, EXCLEQ, LTEQ, LT, GT, GTEQ, PLUSEQ, MINUSEQ, STAREQ, SLASHEQ, PERCENTEQ, ATEQ, AMPEQ, CARETEQ, BAREQ, COLONCOLONEQ, LTLTEQ, GTGTEQ, GTGTGTEQ,  PLUSPLUS, MINUSMINUS, LTLT, GTGT, GTGTGT,  DOTDOT, STARSTAR, QUESTIONCOLON, TILDE, CARET, CARETCARET, BAR, BARBAR, AMP, AMPAMP, QUESTION, COLON, COLONCOLON, LPAR, RPAR, LQB, RQB, LBRACE, RBRACE, COMMA, DOT, DOTCOMMA, SHARP, ELIF, INDENT, SKIP, HTML = range(94)

OPERATOR_CHARS = "+-*/()=;{},<>#&|[]:.@?!%"
OPERATOR_TOKENS = [PLUS, MINUS, STAR, SLASH,
		LPAR, RPAR, EQUAL, DOTCOMMA,
		LBRACE, RBRACE, COMMA, LT, GT,
		SHARP, AMP, BAR, LQB, RQB,
		COLON, DOT, AT, QUESTION, EXCL, PERCENT]

def operator(item):
	return OPERATOR_TOKENS[OPERATOR_CHARS.index(item)]

# MULTIPLE_OPERATORS = {
# 	"==": EQEQ,
# 	">=": GTEQ,
# 	"<=": LTEQ
# }

KEYWORDS = dict()
KEYWORDS["end"] = END

KEYWORDS["static"] = STATIC

KEYWORDS["return"] = RETURN

# KEYWORDS["int"] = NUM
# KEYWORDS["float"] = NUM
# KEYWORDS["double"] = NUM
# KEYWORDS["string"] = STRING
# KEYWORDS["var"] = AUTO

KEYWORDS["lambda"] = FUNCTION
KEYWORDS["func"] = FUNCTION
KEYWORDS["indef"] = FUNCTION
KEYWORDS["redef"] = FUNCTION
KEYWORDS["redefine"] = FUNCTION
KEYWORDS["cdef"] = FUNCTION
KEYWORDS["cpdef"] = FUNCTION
KEYWORDS["def"] = FUNCTION
KEYWORDS["define"] = FUNCTION
KEYWORDS["fn"] = FUNCTION

KEYWORDS["public"] = PUBLIC
KEYWORDS["private"] = PRIVATE
KEYWORDS["protected"] = PROTECTED

KEYWORDS["new"] = NEW

KEYWORDS["class"] = CLASS
KEYWORDS["if"] = IF
KEYWORDS["elif"] = ELIF
KEYWORDS["else"] = ELSE
KEYWORDS["while"] = WHILE
KEYWORDS["for"] = FOR

KEYWORDS["continue"] = CONTINUE
KEYWORDS["break"] = BREAK

KEYWORDS["skip"] = SKIP

class Token(object):
    def __init__(self, type, text):
        self.type = type
        self.text = text
    def __str__(self):
        return str(self.text)
    def __repr__(self):
        return str(self)