
from lexer import *
from parse import *
from nvm import *
from pymodules import *

# sys.argv = ["python", "run.py", '0.0.0.0:920']
def run(filename):
    DEBUG = False
    lexer = Lexer()
    parser = NParser()
    vm = modules(Nvm())
    lines = open(filename, encoding="utf-8").read().split('\n')
    program = str()
    for line in lines:
        ln = str()
        for i, char in enumerate(line):
            if char == '/' and line[i + 1] == '/':
                break
            ln += char
        program += ln
    tokens = lexer.tokenize(program)
    if DEBUG:
        print(f'{tokens}')
    statements = parser.program(tokens)
    for statement in statements:
        statement.eval(vm)

def isaddr(value):
    try:
        f, x = value.split(":")
        v, n, l, z = f.split('.')
        return True
    except:
        return False
if __name__ == '__main__':
    commands = ["run", "makemigrations", "migrate"]
    p = sys.argv[1]
    if isaddr(p):
        from nweb import *
        server = NLangWebServer()
        server.run(ip=p.split(":")[0], port=int(p.split(":")[1]))
    elif p not in commands:
        run(p)