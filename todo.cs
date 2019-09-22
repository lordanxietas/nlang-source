
int define initClass() {
  return class {
    int define x () {
      return 123;
    }
  }
}
int def test () {
  int cdef x () {
    return 'влад' + ' $ ' + 'w';
  }
  return x;
}
int cdef x () {
  return 231;
}
int newfunc = test();
print(newfunc());
return def():
  pass

exec('import json'); //python module
string = '{"hallo": "test"}';
_json = json.loads(string);
print(_json['hallo']); //test

exec('import threading')
threading.Thread(target=getClass).start()

int x = 5;
float y = 10;
double s = (x + y) * 2;
string msg = 'It`s z. Local method';
int define printX () {
  print(x);
}
string func printY () {
  print(y);
  define z () {
    print(msg);
  }
  z();
}
float define printS () {
  print((s / 2));
  printY();
}


printS();
exec('
class Variable:
    def __init__(self):
        pass
    @staticmethod
    def getValue():
        return 123
var = Variable()
print(f"Hello. Variable is {Variable.getValue()}")
');