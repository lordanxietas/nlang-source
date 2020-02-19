from statements import *
from expressions import *
from exceptions import *
from type import *
class NParser(object):
    def __init__(self):
        self.tokens = []
        self.statements = []
        self.size = lambda: len(self.tokens)
        self.position = 0
        self.tablevel = 0

    def program(self, tokens):
        statements = []
        self.tokens = tokens
        while self.position < self.size():
            
            statement = self.statement()
            if statement != None:
                statements.append(statement)
                if self.get(-1).type not in [RBRACE, DOTCOMMA, END, HTML, NLANGSTART, NLANGEND]:
                    self.consume(DOTCOMMA)
                else:
                    self.match(DOTCOMMA)
        return statements

    def statement(self):
        return self.html()
    
    def html(self):
        if self.look(NLANGSTART, -1) and self.look(EQUAL):
            self.next()
            res = EchoExpression(self.getter())
            self.consume(NLANGEND)
            return res
        if self.match(NLANGSTART) or self.match(NLANGEND):
            return None
        if self.look(NLANGEND) and self.look(HTML, 1) and self.look(NLANGSTART, 2):
            self.match(NLANGEND)
            return HtmlExpression(self.consume(HTML).text)
        if self.look(HTML):
            return HtmlExpression(self.consume(HTML).text)
        return self.funcdecl()

    def funcdecl(self):
        if (self.look(VARIABLE)) and self.look(VARIABLE, 1) and self.look(LPAR, 2):
            typeofret = self.get(0).text
            self.next()
            funcname = self.consume(VARIABLE).text
            self.consume(LPAR)
            args = {}
            while not self.match(RPAR):
                type = self.get().text
                self.next()
                name = self.consume(VARIABLE).text
                args[name] = {"type": type, "base": None}
                if self.match(EQUAL):
                    args[name]["base"] = self.expression()
                self.match(COMMA)
            block = self.block()
            return FunctionDeclaration(typeofret, funcname, args, block)
        return self.classdecl()
    
    def classdecl(self):
        if (self.match(CLASS)):
            classname = self.consume(VARIABLE).text
            parents = []
            if self.match(COLON):
                while not self.match(LBRACE):
                    parents.append(self.consume(VARIABLE).text)
                    self.match(COMMA)

            self.match(LBRACE)
            classfields = []
            while not self.match(RBRACE):
                '''Добавляем statements'''
                access = PRIVATE
                static = False
                type = None
                if self.look(PRIVATE) or self.look(PUBLIC) or self.look(PROTECTED):
                    access = self.get(0).type
                    self.next()
                if 'static' in self.get().text:
                    static = True
                    self.next()
                if self.look(VARIABLE):
                    type = self.get(0).text
                    self.next()
                else:
                    type = 'Python';
                    self.next()
                    # raise TypeError('Укажите тип переменной.')
                    pass
                name = self.consume(VARIABLE).text
                if self.match(LPAR):
                    '''Функция'''
                    args = {}
                    while not self.match(RPAR):
                        argtype = self.get(0).text
                        self.next()
                        argname = self.consume(VARIABLE).text 
                        args[argname] = {"type": type, "base": None}
                        if self.match(EQUAL):
                            args[argname]["base"] = self.expression()
                        self.match(COMMA)
                    classfields.append(
                        ClassFunction(classname, access, static, type, name, args, self.block()))
                    self.match(DOTCOMMA)
                elif self.match(EQUAL):
                    '''Поле'''
                    classfields.append(
                        ClassField(access, static, type, name, self.expression()))
                    self.consume(DOTCOMMA)
            # декларируем класс
            return ClassStatement(classname, parents, classfields)
        return self.startsvariable()

    def startsvariable(self):
        current = self.get(0)
        
        if (self.look(VARIABLE)) and self.look(VARIABLE, 1):
            # Декларация
            type = self.get(0).text;self.next();
            name = self.consume(VARIABLE).text
            self.match(EQUAL)
            return DeclarationStatement(type, name, self.expression())
        return self.return_statement()
    
    def return_statement(self):
        if self.match(RETURN):
            expr = self.expression()
            return ReturnStatement(expr)
        if self.look(VARIABLE):
            getter = self.getter()
            if self.match(EQUAL):
                expr = self.expression()
                return AssignmentStatement(getter, expr)
            elif self.look(STAR) and self.look(EQUAL, 1):
                self.next();self.next();
                return BinaryExpression(STAREQ, getter, self.expression())
            elif self.look(SLASH) and self.look(EQUAL, 1):
                self.next();self.next();
                return BinaryExpression(SLASHEQ, getter, self.expression())
            elif self.look(PLUS) and self.look(EQUAL, 1):
                self.next();self.next();
                return BinaryExpression(PLUSEQ, getter, self.expression())
            elif self.look(MINUS) and self.look(EQUAL, 1):
                self.next();self.next();
                return BinaryExpression(MINUSEQ, getter, self.expression())
            elif self.look(PERCENTEQ) and self.look(EQUAL, 1):
                self.next();self.next();
                return BinaryExpression(PERCENTEQEQ, getter, self.expression())
            elif self.look(PLUS) and self.look(PLUS, 1):
                self.next();self.next();
                return BinaryExpression(INCREMENT, getter, 'bt')
            elif self.look(MINUS) and self.look(MINUS, 1):
                self.next();self.next();
                return BinaryExpression(DECREMENT, getter, 'bt')
            return getter
        if self.match(AT):
            return DecoratorStatement(self.getter(), self.statement())
        return self.conditional_statement()

    def conditional_statement(self):
        if self.match(IF):
            self.match(LPAR)
            cond = self.expression()
            self.match(RPAR)
            ifst = BlockStatement(self.block())
            elsest = None
            if self.match(ELSE):
                elsest = BlockStatement(self.block())
            return ConditionalStatement(cond, ifst, elsest)
        return self.for_statement()

    def for_statement(self):
        if self.match(FOR):
            self.match(LPAR)
            if self.get(1).type == COMMA:
                key = self.consume(VARIABLE).text
                self.match(COMMA)
                value = self.consume(VARIABLE).text
                self.consume(COLON)
                expr = self.getter()
                block = BlockStatement(self.block())
                self.match(RPAR)
                return ForeachStatement(key, value, expr, block)
            decl = self.startsvariable()
            self.consume(DOTCOMMA)
            _while = self.expression()
            self.consume(DOTCOMMA)
            _do = self.statement()
            self.match(RPAR)
            block = BlockStatement(self.block())
            return ForStatement(decl, _while, _do, block)
        return self.while_statement()

    def while_statement(self):
        if self.match(WHILE):
            expr = self.expression()
            block = BlockStatement(self.block())
            return WhileStatement(expr, block)
        if ((self.get(0).type in [NUM, STRING] and self.look(DOT, 1)) or self.get(0).type in [LBRACE]):
            res = self.getter()
            
            return res
        raise SyntaxError('Неверный синтаксис')
    

    def block(self):
        statements = []
        try:
            self.consume(LBRACE)
            nexttype = RBRACE
        except:
            if self.match(COLON):
                nexttype = DOTCOMMA
            else:
                return self.statement()
        while not self.match(nexttype):
            st = self.statement()
            self.match(DOTCOMMA)
            self.match(NLANGEND)
            self.match(NLANGSTART)
            statements.append(st)
            if self.look(ELSE):
                break
        return statements

    def expression(self):
        return self.function()
    
    def function (self):

        if self.match(FUNCTION):
            self.consume(LPAR)
            args = {}
            while not self.match(RPAR):
                type = self.get().text
                self.next()
                name = self.consume(VARIABLE).text
                args[name] = {"type": type, "base": None}
                if self.match(EQUAL):
                    args[name]["base"] = self.expression()
                self.match(COMMA)
            block = self.block()
            return FunctionExpression(args, block)

        return self.new()
    
    def new(self):
        if self.match(NEW):
            getter = self.getter()
            return NewExpression(getter, getter.list[0].args)
        return self.funcexpr()
    def funcexpr(self):
        return self.logicalor()

    def logicalor(self):
        result = self.logicaland()
        while True:
            if self.match(BARBAR):
                result = ConditionalExpression(BARBAR, result, self.logicaland())
                continue
            break
        return result

    def logicaland(self):
        result = self.equality()
        while True:
            if self.match(AMPAMP):
                result = ConditionalExpression(AMPAMP, result, self.equality())
                continue
            if self.match(BARBAR):
                result = ConditionalExpression(BARBAR, result, self.equality())
                continue
            break
        return result

    def equality(self):
        result = self.conditional()
        while True:
            if self.match(EQEQ):
                result = ConditionalExpression(EQEQ, result, self.conditional())
                continue
            if self.match(EXCLEQ):
                result = ConditionalExpression(EXCLEQ, result, self.additive())
                continue
            break
        return result

    def conditional(self):
        result = self.additive()
        while True:
            if self.match(LT):
                result = ConditionalExpression(LT, result, self.additive())
                continue
            if self.match(GT):
                result = ConditionalExpression(GT, result, self.additive())
                continue
            if self.match(LTEQ):
                result = ConditionalExpression(LTEQ, result, self.additive())
                continue
            if self.match(GTEQ):
                result = ConditionalExpression(GTEQ, result, self.additive())
                continue
            break
        return result

    def additive(self):
        result = self.multiplicative()
        while True:
            if self.match(PLUS):
                result = BinaryExpression(PLUS, result, self.multiplicative())
                continue
            if self.match(MINUS):
                result = BinaryExpression(MINUS, result, self.multiplicative())
                continue
            break
        return result    

    def multiplicative(self):
        result = self.unary()
        while True:
            if self.look(STAR) and self.look(STAR, 1):
                self.next();self.next();
                result = BinaryExpression(STARSTAR, result, self.unary())
                continue
            if self.look(SLASH) and self.look(SLASH, 1):
                self.next();self.next();
                result = BinaryExpression(DOUBLESLASH, result, self.unary())
                continue
            if self.match(STAR):
                result = BinaryExpression(STAR, result, self.unary())
                continue
            
            if self.match(SLASH):
                result = BinaryExpression(SLASH, result, self.unary())
                continue
            if self.match(PERCENT):
                result = BinaryExpression(PERCENT, result, self.unary())
                continue
            
            
            break
        return result
    
    def unary(self):
        if self.match(MINUS):
            return UnaryExpression(MINUS, self.primary())
        if self.match(PLUS):
            return self.primary()
        return self.getter()
    
    def getter(self):
        # GetterExpression условно говоря если следующий не . то будет заканчивать.
        # Можно так: 1.string()
        getterarr = []
        first = self.primary()
        if self.match(LPAR):
            args = {}
            i = 0
            while not self.match(RPAR):
                if self.look(VARIABLE) and self.look(EQUAL, 1):
                    name = self.consume(VARIABLE).text
                    self.match(EQUAL)
                    args[name] = self.expression()
                else:
                    args[i] = self.expression()
                self.match(COMMA)
                i += 1
            getterarr += [CallingExpression(first, args)]
        else:
            getterarr += [first]
            if self.match(LQB):
                access = []
                access += [self.expression()]
                self.consume(RQB)
                while self.match(LQB):
                    access += [self.expression()]
                    self.consume(RQB)
                getterarr += [ArrayAccessExpression(access)]
        while self.match(DOT):
            if self.look(VARIABLE) and self.look(LPAR, 1):
                var = self.primary()
                self.match(LPAR)
                args = {}
                i = 0
                while not self.match(RPAR):
                    if self.look(VARIABLE) and self.look(EQUAL, 1):
                        name = self.consume(VARIABLE).text
                        self.match(EQUAL)
                        args[name] = self.expression()
                    else:
                        args[i] = self.expression()
                    self.match(COMMA)
                    i += 1
                getterarr += [CallingExpression(var, args)]
            else:
                getterarr += [self.primary()]
        return GetterExpression(getterarr)
    def primary(self):
        current = self.get(0)
        if self.match(NUM):
            return NumberExpression(current.text)
        if self.match(STRING):
            return StringExpression(current.text)
        if self.match(VARIABLE):
            return VariableExpression(current.text)
        if self.match(LQB):
            array = []
            while not self.match(RQB):
                array.append(self.expression())
                self.match(COMMA)
                self.match(DOTCOMMA)
            return ListExpression(array)
        if self.match(EXCL):
            return ExcludeExpression(self.expression())
        if self.match(LBRACE):
            array = {}
            while not self.match(RBRACE):
                # array.append(self.expression())
                name = self.primary()
                self.consume(COLON)
                array[name] = self.expression()
                self.match(COMMA)
                self.match(DOTCOMMA)
            
            return DictExpression(array)

        if self.match(LPAR):
            result = self.expression()
            self.match(RPAR)
            return result
        raise WrongExpressionException('Неправильное выражение')
    def say(self, text):
        self.position -= 1
        print(text)
        return None
    def next(self):
        self.position += 1
    def match(self, type, relativePosition=0):
        current = self.get(0 + relativePosition)
        try:
            if type != current.type:
                return False
        except:
            return False
        self.next()
        return True
    def look(self, type, relativePosition=0):
        current = self.get(0 + relativePosition)
        try:
            if type != current.type:
                return False
        except:
            return False
        return True
    def consume(self, type, relativePosition=0):
        current = self.get(0 + relativePosition)
        try:
            if type != current.type:
                raise WrongSyntaxException('Неверный синтаксис')
        except:
            raise WrongSyntaxException('Неверный синтаксис')
        self.next()
        return current
    def get(self, relativePosition=0):
        position = self.position + relativePosition
        if position >= self.size():
            return None
        return self.tokens[position]
    