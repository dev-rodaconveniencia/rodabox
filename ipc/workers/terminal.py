import daemon

class parser(daemon.Demonize):
  LAST_COMMAND_LINE = ''

  def _update_ethernet(self):
    print("Executando _update_ethernet")

  def _update_wifi(self):
    print("Executando _update_wifi")

  def _update_bluetooth(self):
    print("Executando _update_bluetooth")

  def _update_touch(self):
    print("Executando _update_touch")

  def _update_hdmi(self):
    print("Executando _update_hdmi")

  def _update_barcode(self):
    print("Executando _update_barcode")

  def _update_pinpad(self):
    print("Executando _update_pinpad")


  def _execute_reboot(self):
    print("Executando _execute_reboot")
  def _execute_shutdown(self):
    print("Executando _execute_shutdown")


  def _echo(self):
    print("Executando _echo(")


  def _payment_start(self):
    # pinpad socket
    print("Executando _payment_start")

  def _payment_transaction(self, **value):
    # chamar pinpad via socket
    print("Executando _payment_transaction")

  def _payment_refound(self, **value):
    # pinpad socket
    print("Executando _payment_refound")
