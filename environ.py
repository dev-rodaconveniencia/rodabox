'''
  Este abstrai o os.environ para salvar os dados em .environ. Todos os dados salvos em .environ
  são compartilhados em os.environ para haver interoperatividade entre as camadas de processo.

  Attributes:
    set (None):
      Cria uma variável de ambiente;
    get (str):
      Busca uma variável de ambiente;
    remove (None):
      Remove uma variável de ambiente;
    lazzy (os._Environ):
      Carrega as variáveis de ambiente;
'''
import os
import json

_FILENAME = 'environ'
_FILEPATH = './.%s' % _FILENAME

def set(key, value):
  '''
    Cria uma variável de ambiente.

    Parameters:
    ===========
      key -> str: nome da variável;
      value -> str: valor da variável;

    Return:
    =======
      set -> None;
  '''
  environ = dict()
  with open(_FILEPATH, 'r') as file:
    environ = json.loads(file.read())
  with open(_FILEPATH, 'w') as file:
    environ[key] = str(value)
    json.dump(environ, file, ensure_ascii=False, sort_keys=True, indent=2)
  os.environ[key] = value

def get(key=None):
  '''
    Busca uma variável de ambiente. Caso a variável não exista retorna um KeyError.

    Parameters:
    ===========
      key -> str: nome da variável;

    Exceptions:
    ===========
      KeyError:
        variável não existe.

    Return:
    =======
      get -> str
  '''
  if key == None:
    return dict(os.environ)
  if not key in os.environ.keys():
    raise KeyError("There is no item named '%s' in the archive" % key)
  return os.environ[key]

def remove(key):
  '''
    Remove uma variável de ambiente. Caso a variável não exista retorna um KeyError.

    Parameters:
    ===========
      key -> str: nome da variável;

    Exceptions:
    ===========
      KeyError:
        variável não existe.

    Return:
    =======
      get -> None
  '''
  environ = dict()
  with open(_FILEPATH, 'r') as file:
    environ = json.loads(file.read())
  if not key in environ.keys():
    raise KeyError("There is no item named '%s' in the archive" % key)
  with open(_FILEPATH, 'w') as file:
    environ.pop(key)
    os.environ.pop(key)
    json.dump(environ, file, ensure_ascii=False, sort_keys=True, indent=2)

def lazzy():
  '''
    Carrega as variáveis de ambiente

    Return:
    =======
      lazzy -> os._Environ
  '''
  copy = os.environ.copy()
  with open(_FILEPATH, 'r') as file:
    environ = json.loads(file.read())
  for key, value in environ.items():
    copy[key] = str(value)
  return copy
