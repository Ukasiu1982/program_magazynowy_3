from main import manager
import sys

a = sys.argv[2]
b = sys.argv[3]
c = sys.argv[4]
manager.execute("sprzedaz", a, int(b), int(c))
manager.zapis("sprzedaz", a, b, c)
