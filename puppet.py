'''
  Start dos serviços de telemetria.

  Este método faz a primeira ponta de ligação com a abertura dos serviços de telemetria, banco de
  dados local, processos externos e backlogs. Todos os serviços abertos aqui tem em comum a classe
  os.environ como canal comum de comunicação.

  Attributes:
    _wait_for_any (None):
      Inicia todos os serviços de telemetria.

    ask_for_authentication (bool):
      Busca por autenticação no banco watchman.

    check_github_updates (bool):
      Busca por atualizações no github.

    backpack_service (None):
      Inicia o subprocesso backpack.

    ipc_service (None):
      Inicia o subprocesso ipc.

    pinpad_service (None):
      Inicia o subprocess pinpad.
'''

import os
import json
import time
import uuid
import requests
import threading
import subprocess
import setproctitle

import environ
import scrubs

from datetime import datetime
from sh import git, reboot, python, kill

setproctitle.setproctitle('rodabox-puppet')

_PIDS = list()
DEBUG = True

def _wait_for_any(handles):
  '''Aqui irá acontecer o start de todos os serviços'''
  print("[Rodabox - %s] - all processes are started." % str(datetime.now()))
  for handle in handles:
    handle.start()

  while True:
    try:
      input()
      # Caso o teclado faça uma iterrupção, mata todos os processos e reinicia a maquina
    except KeyboardInterrupt as ex:
      for handle in handles:
        handle.join()
      exit()
      if not DEBUG:
        reboot()

@scrubs.handle.exception
def ask_for_authentication():
  """
  Pede autorização para o watchman para começar a operar.
  Isso só acontecerá se o box não estiver cadastrado no sistema watchman. Para operar, a variável
  RODABOX_WAS_VALIDATED tem que ser True e o RODABOX_TOKEN_WATCHMAN deve estar preenchido. Caso
  o totem mude, a tentativa de autenticação se manterá.
  """
  macaddress = hex(uuid.getnode())
  ask = {
    "address" : "http://%s:%s/ask_for_authentication" % (
      environ.get("RODABOX_SERVER_API_HOST"),
      environ.get("RODABOX_SERVER_API_PORT")
    ),
    "params" : {
      "macaddress": macaddress
    },
    "headers": {
      'content-type': 'application/json'
    }
  }
  token = {
    "address": "http://%s:%s/api/v1/auth/token/login" % (
      environ.get("RODABOX_SERVER_API_HOST"),
      environ.get("RODABOX_SERVER_API_PORT")
    ),
    "data": {
      "email": "%s@rodaconveniencia.com.br" % macaddress,
      "password": macaddress
    },
    "headers": {
      'content-type': 'application/json'
    }
  }

  response = requests.get(ask["address"], params=ask["params"], headers=ask["headers"])

  if response.status_code == requests.codes.ok:
    askResp = response.json()
    if askResp["isregistered"]:
      # Se o totem foi registrado, guarda a nova chave de acesso para usar posteriormente na sincro-
      # nização dos dados.
      data_stringfy = json.dumps(token["data"])
      response = requests.post(token["address"], data=data_stringfy, headers=token["headers"])
      tokenResp = response.json()
      environ.set("RODABOX_TOKEN_WATCHMAN", "Token %s" % tokenResp["auth_token"])
      environ.set("RODABOX_LAST_LOGIN", str(datetime.now()))
      return True
  else:
    raise Exception("Status response return '%s'." % response.status_code)

@scrubs.handle.exception
def check_github_updates():
  '''
  Busca atualizações do pacote no github. Ao fazer isso, automaticamente mudará a versão no
  aquivo environ. Este sistema de atualização automatica irá acontecer todos os dias as 3am.
  Para a operação de reboot acontecer, o crontab foi definido para reboot todos os dias as 3am.
  Ao iniciar este serviço, a atualização será dada automaticamente. Se houver atualização o
  sistema irá reiniciar logo em seguida.
  '''
  shell = 'pull https://%s:x-oauth-basic@github.com/rodaconveniencia/rodabox.git master' % (
    environ.get('RODABOX_TOKEN_GITHUB')
  )
  stdout = git(shell.split()).strip()
  return not stdout.startswith('Already up to date.')

@scrubs.handle.exception
def backpack_service():
  ''' Inicia o django em background '''
  shell = 'python ./backpack/manage.py runserver %s:%s' % (
    environ.get('RODABOX_SERVER_BACKPACK_HOST'),
    environ.get('RODABOX_SERVER_BACKPACK_PORT')
  )
  process = subprocess.Popen(shell.split(), env=os.environ)
  _PIDS.append(process.pid)

@scrubs.handle.exception
def ipc_service():
  ''' Inicia o ipc em background '''
  shell = 'python ./ipc/manage.py demonize %s:%s' % (
    environ.get('RODABOX_SERVER_IPC_HOST'),
    environ.get('RODABOX_SERVER_IPC_PORT')
  )
  process = subprocess.Popen(shell.split(), env=os.environ)
  _PIDS.append(process.pid)

@scrubs.handle.exception
def pinpad_service():
  ''' Inicia o pinpad em background '''
  shell = 'mono ./pinpad/bin/Debug/SimpleConsoleApp.exe'
  process = subprocess.Popen(shell.split())
  _PIDS.append(process.pid)

if __name__ == '__main__':
  # Todas as threads entraram nesta lista para debug
  handles = list()
  # Carrega o environment junto com o arquivo .environ
  os.environ = environ.lazzy()

  # checa por atualizações no github
  if check_github_updates():
    # Se houver atualizações, atualiza o .environ com a data e hora da atualização e o hash do
    # último commit. Depois faz a migração no banco de dados.
    environ.set('RODABOX_UPDATED_AT', str(datetime.now()))
    environ.set('RODABOX_LAST_GIT_COMMIT', git("rev-parse HEAD".split()).strip())
    python("./backpack/manage.py makemigrations".split())
    python("./backpack/manage.py migrate".split())
    if not DEBUG:
      # Se não estiver em ambiente de testes, faz o reboot.
      reboot()

  # Busca pela autenticação no servidor. Caso o raspberry esteja cadastrado, faz o login e pede o
  # token de autenticação. Depois guarda o token no .environ. Caso não haja autenticação, o servidor
  # irá mostrar ao manager que um usuário pediu autenticação.

  # TODO: PEP572
  # while (token := ask_for_authentication()) is not True:
  #   if token != None:
  #     environ.set('RODABOX_TOKEN_WATCHMAN', token)
  #   time.sleep(1)

  while True:
    token = ask_for_authentication()
    if token != None:
      environ.set('RODABOX_TOKEN_WATCHMAN', token)
      break
    time.sleep(1)

  # Abre todos os serviços em threads
  # handles.append(threading.Thread(target=pinpad_service))
  handles.append(threading.Thread(target=ipc_service))
  # handles.append(threading.Thread(target=backpack_service))

  # Espera a iterrupção do teclado
  _wait_for_any(handles)
