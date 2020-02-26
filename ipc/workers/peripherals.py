import daemon
import subprocess
import time

class status(daemon.Demonize):

  def _list_devices(self):
    devices = list()
    bash = "lsusb"
    process = subprocess.run(bash.split(), capture_output=True)
    stdout = process.stdout.decode('utf-8')
    for device in stdout.splitlines():
      model = { 'Bus': None, 'Device': None, 'ID': None, 'Description': None }
      model['bus'] = device[4:7]
      model['device'] = device[15:18]
      model['id'] = device[23:32]
      model['description'] = device[33:]
      devices.append(model)
    return self.response(devices)

  def hasEthernet(self):
    bash = '/bin/cat /sys/class/net/eth0/carrier'
    process = subprocess.run(bash.split(), capture_output=True)
    stdout = process.stdout.decode('utf-8')
    return self.response(bool(int(stdout)))

  def hasHotPlugWifi(self):
    for device in self._list_devices():
      if 'wireless' in device['description'].lower():
        return self.response(True, wait=0.1)
    return self.response(False, wait=0.1)

  def hasBluetooth(self):
    for device in self._list_devices():
      if 'bluetooth' in device['description'].lower():
        return self.response(True)
    return self.response(False)

  def hasGPRS(self):
    for device in self._list_devices():
      if 'd-link corp' in device['description'].lower():
        return self.response(True)
    return self.response(False)

  def hasTouch(self):
    for device in self._list_devices():
      if 'd-wav' in device['description'].lower():
        return self.response(True)
    return self.response(False)

  def hasHDMI(self):
    bash = 'tvservice -n'
    process = subprocess.run(bash.split(), capture_output=True)
    stdout = process.stdout.decode('utf-8')
    if not stdout is '':
      return self.response(True)
    return self.response(False)

  def hasBarcode(self):
    for device in self._list_devices():
      if 'barcode' in device["description"].lower():
        return self.response(True)
    return self.response(False)

  def hasPinpad(self):
    pinpads = [
      "GERTEC Telecomunicacoes Ltda",
      "Sagem"
    ]
    for device in self._list_devices():
      for pinpad in pinpads:
        if device["description"].startswith(pinpad):
          return self.response(True)
    return self.response(False)

  def temperature(self):
    bash = '/opt/vc/bin/vcgencmd measure_temp'
    process = subprocess.run(bash.split(), capture_output=True)
    stdout = process.stdout.decode('utf-8')
    return self.response("%s°C" % re.findall(r'\d+', stdout)[0])

  def voltage(self):
    bash = '/opt/vc/bin/vcgencmd measure_volts core'
    process = subprocess.run(bash.split(), capture_output=True)
    stdout = process.stdout.decode('utf-8')
    return self.response("%sV" % ''.join(re.findall(r'\d+', stdout)))
