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

if not os.path.isfile(_FILEPATH):
  default_file_string = '''
    {
      "RODABOX_LAST_GIT_COMMIT": "",
      "RODABOX_LAST_LOGIN": "",
      "RODABOX_PROJECT_AUTHOR": "Roda Conveniência Laboratory",
      "RODABOX_PROJECT_NAME": "rodabox",
      "RODABOX_PROJECT_VERSION": "0.0.1",
      "RODABOX_SERVER_API_HOST": "0.0.0.0",
      "RODABOX_SERVER_API_PORT": "5000",
      "RODABOX_SERVER_BACKPACK_HOST": "0.0.0.0",
      "RODABOX_SERVER_BACKPACK_PORT": "8000",
      "RODABOX_SERVER_IPC_HOST": "0.0.0.0",
      "RODABOX_SERVER_IPC_PORT": "6000",
      "RODABOX_SERVER_PINPAD_HOST": "0.0.0.0",
      "RODABOX_SERVER_PINPAD_PORT": "7000",
      "RODABOX_TOKEN_GITHUB": "c309669c01a4c98920562364a40e64fd82c7b71a",
      "RODABOX_TOKEN_WATCHMAN": "",
      "RODABOX_UPDATED_AT": "",
      "RODABOX_WAS_VALIDATED": ""
    }
  '''
  file = open(_FILEPATH, 'w')
  file.write(default_file_string)
  file.close()

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
