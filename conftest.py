import sys

# Mock microcontroller UID attribute to "1337d00d"
my_microcontroller = type(sys)("microcontroller")
my_microcontroller.cpu = type(sys)("cpu")
my_microcontroller.cpu.uid = bytearray(b"\x13\x37\xd0\x0d")
sys.modules["microcontroller"] = my_microcontroller
my_micropython = type(sys)("micropython")


def my_const(value):
    return value


my_micropython.const = my_const

sys.modules["micropython"] = my_micropython
