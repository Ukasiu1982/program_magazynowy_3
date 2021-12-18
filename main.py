import sys


class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.history = []

    def read_lines(self):
        with open(self.file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line == "stop":
                    break
                try:
                    line = float(line)
                except ValueError:
                    pass
                self.history.append(line)

    def save_lines(self, new_content):
        with open(self.file_path, "w") as file:
            file.writelines([str(line)+'\n' for line in new_content])

    def __print(self):
        print(self.history)


class Manager:
    def __init__(self, file_handler):
        self.actions = {}
        self.account = 0
        self.storage = {}
        self.history = file_handler.history
        self.zapis_zdarzen = []

    def assign(self, name):
        def decorate(func):
            self.actions[name] = func
        return decorate

    def execute(self, name, *args, **kwargs):
        if name not in self.actions:
            raise Exception
        self.actions[name](self, *args, **kwargs)

    def zapis(self, *args):
        with open("zapis.txt", "w") as f:
            for komenda in self.history:
                for akcja in komenda:
                    f.write(str(akcja)+ "\n")
            if args:
                f.writelines([element + '\n' for element in args])
            f.write("stop")

    def dzialanie_magazynu(self, identifier, value, quantity):
        if quantity < 0:
            if identifier in self.storage:
                if (self.storage.get(identifier) + quantity) >= 0:
                    self.storage[identifier] = self.storage.get(identifier) + quantity
                else:
                    print("Brak wystarczajacej ilosci {}  w magazynie".format(identifier))
                    return False
            else:
                print("Brak produktu")
                return False
        else:
            if identifier in self.storage:
                self.storage[identifier] = self.storage.get(identifier) + quantity
            else:
                self.storage[identifier] = quantity

    def zapis_akcji(self, action, parameters):
        self.zapis_zdarzen.append({'action': action, "parameters": tuple(parameters)})

    def pobranie_danych(self):     #czytanie akcji
        historia = []
        komenda = []
        for akcja in self.history:
            if akcja in ["saldo", "zakup", "sprzedaz"]:
                if komenda:
                    self.execute(komenda[0], *komenda[1:])
                    historia.append(komenda)
                komenda = []
            komenda.append(akcja)
        historia.append(komenda)
        self.history = historia



fh = FileHandler(sys.argv[1])
fh.read_lines()

manager = Manager(fh)


@manager.assign("konto")
def account(manager, *args, **kwargs):
    print(f'Stan konta: {manager.account}')

@manager.assign("saldo")
def saldo(manager, accountant_change, *args, **kwargs):
    if manager.account + accountant_change >= 0:
        manager.account += accountant_change

@manager.assign("przeglad")
def przeglad(manager, start, end, *args, **kwargs):
    print(manager.history[start:end+1])

@manager.assign("zakup")
def zakup(manager, identifier, value, quantity,  *args, **kwargs):
    if value > 0 and quantity > 0:
        if (manager.account - (quantity * value)) > 0:
            manager.dzialanie_magazynu(identifier, value, quantity)
            manager.account -= (value * quantity)
            manager.zapis_akcji("sprzedaz",[identifier, value, quantity])
            return True
        else:
            print("brak srodkow")
        return False
    else:
        print("Zle dane")
        return False

@manager.assign("sprzedaz")
def sprzedaz(manager, identifier, value, quantity, *args, **kwargs):
    if value > 0 and quantity > 0:
        if manager.dzialanie_magazynu(identifier, value, quantity * (-1)):
            manager.account += (value * quantity)
            manager.zapis_akcji("sprzedaz", [identifier, value, quantity])
            return True
        else:
            return False
    else:
        print("Zle dane")
        return False


@manager.assign("magazyn")
def magazyn(manager, identifier, *args, **kwargs):
    for product in identifier:
        if product in manager.storage:
            stan = manager.storage.get(product)
        else:
            stan = 0
        print("{}: {}".format(product, stan))


manager.pobranie_danych()

if __name__ == "__main__":
    print(manager.history)