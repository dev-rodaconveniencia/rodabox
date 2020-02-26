from pprint import pprint as print

import os
import json
import socket
import random

import daemon

class transaction(daemon.Demonize):
  PINPAD_SOCKET_ADDRESS = ('localhost', 9000)
  PINPAD_STONECODE = '164185121'
  DEFAULT_BYTES_TRANSPORT_LEN = int(os.environ["DEFAULT_BYTES_TRANSPORT_LEN"])

  def _wise_response(self, response):
    response = json.loads(response)
    wise = dict()
    for _bad_response in response:
      wise.update(_bad_response)
    return wise

  def pay(self):
    if self.scheduler['TERMINAL_PARSER_HASCOMMANDLINE']:
      if 'RODABOX_START_TRANSACTION' in self.scheduler["TERMINAL_LAST_COMMAND_LINE"]:
        value = self.scheduler["TERMINAL_LAST_COMMAND_LINE"].split()[-1]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
          # Conecta ao socket do pinpad
          channel.connect(self.PINPAD_SOCKET_ADDRESS)
          # Ativa o stone code e inicia a máquina
          # Espera a resposta da ativação
          active_message = 'ativar --stonecode %s' % self.PINPAD_STONECODE
          channel.send(active_message.encode())
          stdout = channel.recv(self.DEFAULT_BYTES_TRANSPORT_LEN)
          # Inicia uma transação com um hash aleatório
          # Espera a resposta da transação
          hash = "%032x" % random.getrandbits(128)
          pay_message = 'pagar --valor 0.01 -id %s' % hash.upper()
          channel.send(pay_message.encode())
          stdout = channel.recv(self.DEFAULT_BYTES_TRANSPORT_LEN).decode('utf-8')
          # Espera o resultado da transação
          response = self._wise_response(stdout)
          self.scheduler['TERMINAL_PARSER_HASCOMMANDLINE'] = False
          self.scheduler['RODABOX_LAST_TRANSACTION'] = json.dumps(response)
    return self.response(None)

  def refound(self):
    if self.scheduler['TERMINAL_PARSER_HASCOMMANDLINE']:
      if 'RODABOX_REFOUND_TRANSACTION' in self.scheduler["TERMINAL_LAST_COMMAND_LINE"]:
        stoneid, value = self.scheduler["TERMINAL_LAST_COMMAND_LINE"].split()[1:]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
          # Conecta ao socket do pinpad
          channel.connect(self.PINPAD_SOCKET_ADDRESS)
          # Ativa o stone code e inicia a máquina
          # Espera a resposta da ativação
          active_message = 'ativar --stonecode %s' % self.PINPAD_STONECODE
          channel.send(active_message.encode())
          stdout = channel.recv(self.DEFAULT_BYTES_TRANSPORT_LEN)
          # Inicia uma transação com um hash aleatório
          # Espera a resposta da transação
          pay_message = 'cancelar --stoneid %s --valor %s' % (stoneid, value)
          channel.send(pay_message.encode())
          stdout = channel.recv(self.DEFAULT_BYTES_TRANSPORT_LEN).decode('utf-8')
          # Espera o resultado da transação
          response = self._wise_response(stdout)
          self.scheduler['TERMINAL_PARSER_HASCOMMANDLINE'] = False
          self.scheduler['RODABOX_LAST_TRANSACTION'] = json.dumps(response)
    return self.response(None)
