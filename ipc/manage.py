import os
import sys
import daemon
import setproctitle

setproctitle.setproctitle('rodabox-ipc-daemon')

if __name__ == '__main__':
  _, hang, server = sys.argv
  host, port = server.split(":")

  exec("daemon.{hang}('{host}', {port}).workit()".format(
    hang=hang, host=host, port=port
  ))
