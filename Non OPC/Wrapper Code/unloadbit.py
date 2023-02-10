from pywrapper import *

# Create a handle for the c library
handle = c_lib._handle

#Unload the DLL file
ctypes.windll.kernel32.FreeLibrary(handle)