import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/csanimatronics/CS_Animatronics/src/install/motor_controller'
