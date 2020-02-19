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
class Die(Exception):pass

def cfg(path=''):
    config = {
        "DirectoryIndex": "index.n",
        "PugTranslation": False,
        "deny": [
            "__pycache__", ".vscode", "config.n", ".config",
        ]
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
        sys.path.insert(1, os.getcwd())
        app = flask.Flask(__name__, static_url_path='', static_folder='', template_folder='')
        app.secret_key = 'weartrynbvs34etvfsetc43vrpesrsecrcerv4ervgcrdvsrvy5dhvrt'
        @app.before_request
        def before_request():
            config = cfg()
            result = ''
            filename = None
            uri = flask.request.environ["PATH_INFO"]
            if uri != '/':
                def getfilename(config, uri):
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
                            for ignore in config.get('deny'):
                                if ignore in filepath:
                                    raise NotFound()
                            return flask.send_file(_filename, conditional=True)
                    return None
                filename = getfilename(config, uri)
                if type(filename) != str:
                    return filename
            else:
                filename = config.get('DirectoryIndex')
            if filename != None:
                for ignore in config.get('deny'):
                    if ignore in filename:
                        raise NotFound()
                return self.request(filename, config)
        self.app = app
    def run(self, ip, port):
        self.app.run(ip, port=port, debug=True)
    
    def nlang(self, vm, text):
        result = str()
        lexer = Lexer()
        parser = NParser()
        
        def echo(vm, txt):
            vm['___result___']._value += str(txt)
        vm.lock()
        vm['___result___'] = NObject("")
        vm['echo'] = NObject(lambda txt: echo(vm, txt))

        program = "<?" + str(text)
        lines = program.split('\n')
        nowstr = False
        for line in lines:
            ln = str()
            for i, char in enumerate(line):
                if char in ["'", '"', '`']:
                    nowstr = False if nowstr == True else True
                if char == '#':
                    if not nowstr:
                        break
                ln += char
            program += ln + '\n'
        tokens = lexer.tokenize(program)
        statements = parser.program(tokens)
        for statement in statements:
            statement.eval(vm)
        res = vm['___result___'].nval()
        vm.unlock()
        return res

    def include(self, vm, filename, config):
        result = str()
        lexer = Lexer()
        parser = NParser()
        def echo(vm, text):
            vm['___result']._value += str(text)
        
        try:
            lines = open(filename, encoding="utf-8").read().split('\n')
        except:
            raise NotFound('File ' + filename + ' not found at this server')
        program = str()
        nowstr = False
        for line in lines:
            ln = str()
            for i, char in enumerate(line):
                if char in ["'", '"', '`']:
                    nowstr = False if nowstr == True else True
                if char == '#':
                    if not nowstr:
                        break
                ln += char
            program += ln + '\n'
        tokens = lexer.tokenize(program)
        statements = parser.program(tokens)
        for statement in statements:
            statement.eval(vm)
        if config.get("PugTranslation"):
            return pypugjs.simple_convert(vm['___result']._value)
        else:
            return str(vm['___result']._value)

    def request(self, filename, config):
        result = str()
        DEBUG = False
        lexer = Lexer()
        parser = NParser()
        vm = modules(Nvm())
        vm['___result'] = NObject(str())
        def echo(vm, text):
            vm['___result']._value += str(text)
        def include(filename):
            return self.include(vm, filename, config)
        def location(location):
            raise Redirect(location)
        def die(vm):
            raise Die()
        
        def sha1(text):
            return hashlib.sha1(bytes(text, 'utf-8')).hexdigest()
        
        def session(key, value='none'):
            if value != 'none':
                flask.session[key] = value
            else:
                return flask.session.get(key)

        vm['session'] = NObject(session)
        vm['sha1'] = NObject(sha1)
        vm['redirect'] = NObject(location)
        vm['die'] = NObject(value=lambda:die(vm))
        vm['include'] = NObject(include, static=True)
        vm['echo'] = NObject(lambda text: echo(vm, text), static=True)
        vm['POST'] = NObject(dict(flask.request.form))
        vm['GET'] = NObject(dict(flask.request.args))
        vm['nlang'] = NObject(lambda text: self.nlang(vm, text))
        try:
            lines = open(filename, encoding="utf-8").read().split('\n')
        except:
            raise NotFound('File ' + filename + ' not found at this server')
        program = str()
        nowstr = False
        for line in lines:
            ln = str()
            for i, char in enumerate(line):
                if char in ["'", '"', '`']:
                    nowstr = False if nowstr == True else True
                if char == '#':
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
            except Die:
                break
            except Redirect as e:
                return flask.redirect(e.get())
        if config.get("PugTranslation"):
            return pypugjs.simple_convert(vm['___result']._value)
        else:
            return str(vm['___result']._value)