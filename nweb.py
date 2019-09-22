from webn.lexer import *
from webn.parse import *
from nvm import *
from pymodules import *
import flask
import pypugjs
# print(pypugjs.simple_convert('''
# h1() Hello world!
# '''))
from flask import *
import os.path
from werkzeug.exceptions import BadRequest, NotFound
class Redirect(Exception):

    def __init__(self, text):
        self.text = text
    def get(self):
        return self.text

def cfg(path=''):
    config = {
        "DirectoryIndex": "index.n",
        "PugTranslation": False
    }
    if path != '':
        path += "/"
    try:
        config = json.loads(open(path + ".config").read())
    except:
        open(path + ".config", 'w+').write(json.dumps(config, ensure_ascii=False, indent=4, sort_keys=True))
    return config

class NLangWebServer(object):
    def __init__(self):
        
        app = flask.Flask(__name__, static_url_path='', static_folder='', template_folder='')
        @app.before_request
        def before_request():
            config = cfg()
            result = ''
            filename = None
            uri = flask.request.environ["PATH_INFO"]
            if uri != '/':
                def getfilename(uri):
                    uri = uri[1:]
                    if os.path.isdir(uri):
                        _cfg = cfg(uri)
                        config = _cfg
                        return uri + '/' + _cfg.get('DirectoryIndex')
                    elif uri[len(uri) -2:] == '.n':
                        # raise NotFound()
                        return uri
                    else:
                        '''Листуем директорию и ищем возможный .n файл'''
                        spl = uri.split('/')
                        path = '/'.join(spl[:(len(spl)-1)])
                        _filename = '/'.join(spl[(len(spl)-1):])
                        if '.' not in _filename:
                            if _filename == '':
                                fn = f'{_filename}.n'
                            else:
                                fn = f'/{_filename}.n'
                            if path == '':
                                fn = fn.replace('/', '')
                            return path + fn
                        else:
                            # print(path + _filename)
                            filepath = str(_filename)
                            try:
                                if path[0] != '/':
                                    filepath = path + '/' + _filename
                            except:
                                pass
                            try:
                                if not os.path.isfile(filepath):
                                    raise NotFound()
                            except (TypeError, ValueError) as e:
                                raise flask.BadRequest()
                            global current_app
                            current_app.root_path = path
                            return flask.send_file(_filename, conditional=True)
                    return None
                filename = getfilename(uri)
                if type(filename) != str:
                    return filename
            else:
                filename = config.get('DirectoryIndex')
            if filename != None:
                return self.request(filename, config)
        self.app = app
    def run(self, ip, port):
        self.app.run(ip, port=port, debug=True)

    def include(self, vm, filename, config):
        result = str()
        lexer = Lexer()
        parser = NParser()
        def echo(vm, text):
            vm['result']._value += str(text)
        
        lines = open(filename, encoding="utf-8").read().split('\n')
        program = str()
        nowstr = False
        for line in lines:
            ln = str()
            for i, char in enumerate(line):
                if char in ["'", '"', '`']:
                    nowstr = False if nowstr == True else True
                if char == '/' and line[i + 1] == '/':
                    if not nowstr:
                        break
                ln += char
            program += ln + '\n'
        tokens = lexer.tokenize(program)
        statements = parser.program(tokens)
        for statement in statements:
            statement.eval(vm)
        if config.get("PugTranslation"):
            return pypugjs.simple_convert(vm['result']._value)
        else:
            return str(vm['result']._value)

    def request(self, filename, config):
        result = str()
        DEBUG = False
        lexer = Lexer()
        parser = NParser()
        vm = modules(Nvm())
        vm['result'] = NObject(str())
        def echo(vm, text):
            vm['result']._value += str(text)
        def include(filename):
            return self.include(vm, filename, config)
        def header(location):
            raise Redirect(location)
        def die(vm):
            return vm['result']
        vm['header'] = NObject(header)
        vm['die'] = NObject(value=lambda:die(vm))
        vm['include'] = NObject(include, static=True)
        vm['echo'] = NObject(lambda text: echo(vm, text), static=True)
        vm['POST'] = NObject(dict(flask.request.form))
        vm['GET'] = NObject(dict(flask.request.args))
        lines = open(filename, encoding="utf-8").read().split('\n')
        program = str()
        nowstr = False
        for line in lines:
            ln = str()
            for i, char in enumerate(line):
                if char in ["'", '"', '`']:
                    nowstr = False if nowstr == True else True
                if char == '/' and line[i + 1] == '/':
                    if not nowstr:
                        break
                ln += char
            program += ln + '\n'
        tokens = lexer.tokenize(program)
        if DEBUG:
            print(f'{tokens}')
        statements = parser.program(tokens)
        for statement in statements:
            try:
                statement.eval(vm)
            except Redirect as e:
                return flask.redirect(e.get())
        if config.get("PugTranslation"):
            return pypugjs.simple_convert(vm['result']._value)
        else:
            return str(vm['result']._value)