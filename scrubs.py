'''
  Este módulo faz a recepção dos erros durante a inicialização de algum processo prioritário.
  O módulo não requer conexão com a internet para captar os erros.
  Todos as excessões são salvas em .scrubs .

  Attributes:
    register (None):
      Registra o erro no arquivo .scrubs.
    handle (function):
      Decorador para pegar a excessão.

  Todo:
    * implementar o pull request em targetit -> None;
'''

import os
import json
from datetime import datetime

_FILENAME = 'scrubs'
_FILEPATH = './.%s' % _FILENAME

def register(message):
  '''Registra a excessão em .scrubs'''
  if not os.path.isfile(_FILEPATH):
    file = open(_FILEPATH, 'w')
    file.write('[]')
    file.close()
  with open(_FILEPATH, 'r') as file:
    scrubs = json.load(file)
  scrubs.append(dict(at=str(datetime.now()), exception=message))
  with open(_FILEPATH, 'w') as file:
    json.dump(scrubs, file, ensure_ascii=True, sort_keys=True, indent=2)

def targetit(message):
  '''Abre um pull request no github'''
  raise NotImplementedError

class handle:
  '''decorador para tratar excessões'''
  @classmethod
  def exception(self, function):
    '''excessões gerais'''
    def wrapper(*args, **kwargs):
      try:
        return function(*args, **kwargs)
      except Exception as ex:
        register(str(ex))
        return None
    return wrapper
