from main import manager
import sys

a = sys.argv[2]
b = sys.argv[3]
manager.execute("saldo", int(a), b)
manager.zapis("saldo", a, b)
