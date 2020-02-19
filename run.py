
from lexer import *
from parse import *
from nvm import *
from pymodules import *

class SiteAlreadyCreated(Exception):pass
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
            if char == '#':
                break
            ln += char
        program += ln
    tokens = lexer.tokenize(program)
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
    commands = ["makemigrations", "migrate"]
    p = sys.argv[1]
    if isaddr(p):
        from nweb import *
        server = NLangWebServer()
        server.run(ip=p.split(":")[0], port=int(p.split(":")[1]))
    elif p == 'newsite':
        import os.path
        if os.path.exists('.config'):
            raise SiteAlreadyCreated('The Nlang site already created in this folder')
        os.system('virtualenv venv')
        os.system('venv/bin/pip install flask sqlalchemy flask_sqlalchemy flask_migrate requests pypugjs mysqlclient')
        open('index.n', 'w+', encoding='utf-8').write('''<?
include('db.n');
echo("Hello world");
''')
        os.mkdir('engine')
        os.mkdir('include')
        open('config.n', 'w+', encoding='utf-8').write('''<?
String DB_HOST     = 'localhost';
String DB_USER     = '';
String DB_NAME     = '';
String DB_PASSWORD = '';
''')
        open('db.n', 'w+', encoding='utf-8').write('''<?
include('config.n');
pyimport('MySQLdb');
pyimport('MySQLdb', ['cursors']);

Python conn = MySQLdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, cursorclass=MySQLdb.cursors.DictCursor);
Python sql = conn.cursor();

sql.execute('SET names "utf8"');
''')
        print('''

Hello. We are created new site and installed nlang for you.
For activate the env do ". venv/bin/activate"

''')

    elif p == 'launch':
        print('Do ". venv/bin/activate"')
    elif p not in commands:
        run(p)