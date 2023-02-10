from pywrapper import *

def closeUsb():
	return(c_lib.Balls_usb_close())

def 