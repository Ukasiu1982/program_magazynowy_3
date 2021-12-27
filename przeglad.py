from main import manager
import sys

a = int(sys.argv[2])
b = int(sys.argv[3])
manager.execute("przeglad", a, b)