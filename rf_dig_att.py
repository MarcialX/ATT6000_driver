"""
rf_dig_att.py
Marcial Becerril INAOE november 2018. Based in Sam Rowe's code

This class provides methods to set and get the attenuation level of
the variable attenuator.

e.g. instantiate object. To check the port use dmesg in Linux
>>> att_device = Attenuator(port)

e.g. print attenuator model
>>> print att_device.get_model()

e.g. set the attenuation level
>>> att_device.set_att(5.25)

e.g. get the attenuation level
>>> att_device.get_att()
"""

import serial

#Serial Parameters
BAUDRATE = 115200
NBITS = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOP = serial.STOPBITS_ONE

#Attenuation parameters
ATT_MAX     = 31.75
ATT_MIN     = 0.0
RESOLUTION  = 0.25

class Attenuator(object):
	
	def __init__(self,port):
		self._att = None
		self.model_name = None
		self._port = port

		self.device = serial.Serial(None, timeout=0.01)
		self.device.port = self._port
		self.device.baudrate = BAUDRATE
		self.device.bytesize = NBITS
		self.device.parity = PARITY
		self.device.stopbits = STOP

		try:
			self.openPort()
		except:
			print "Error. Port is not available, check the connection."
			return

		self.model_name = self._get_device_model_name()

	def openPort(self):
		self.device.open()	

	def closePort(self):
		self.device.close()

	def get_att(self):
		"""
		self.device.write("rv0" + "\n")
		while self.device.in_waiting == 0:
			pass
		att_value = self.device.readlines()
		self._att = att_value
		"""
		return self._att
	
	def set_att(self,value):
		assert value <= ATT_MAX, 'Attenuation over range!'
		assert value >= ATT_MIN, 'Attenuation under range!'
		assert (value/RESOLUTION)%1==0, 'Resolution is %.2f dB!'%RESOLUTION
		
		att_value = str(int(100*value))

		self.device.write("wv0" + att_value.zfill(4) + "\n")
		self._att = value
		
		print 'Attenuator set to %.2f dB'%(self._att)
		
	def _get_device_model_name(self):
		self.device.reset_input_buffer()
		self.device.write("rid\n")
		while self.device.in_waiting == 0:
			pass
		model = self.device.readlines()[0]
		return model

	def get_model(self):
		return self.model_name
	
	def get_status(self):
		if self.device.is_open:
			return 'Connected.'
		else:
			return 'Not Connected.'

#port = "/dev/ttyUSB0"
#atten = Attenuator(port)
