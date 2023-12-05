import sys

# Mock microcontroller UID attribute
my_microcontroller = type(sys)("microcontroller")
my_microcontroller.cpu = type(sys)("cpu")
my_microcontroller.cpu.uid = bytearray(b"\x13\x37\xd0\x0d")
sys.modules["microcontroller"] = my_microcontroller
