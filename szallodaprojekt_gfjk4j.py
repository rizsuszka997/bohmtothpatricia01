from abc import ABC, abstractmethod
from datetime import datetime, date, timedelta

# Absztrakt Szoba osztály
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def szoba_tipusa(self):
        pass

# EgyagyasSzoba osztály
class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)

    def szoba_tipusa(self):
        return 'egyágyas'

# KetagyasSzoba osztály
class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)

    def szoba_tipusa(self):
        return 'kétágyas'

# Szalloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
    
    def szoba_hozzaadasa(self, szoba):
        self.szobak.append(szoba)

# Foglalas osztály
class Foglalas:
    def __init__(self, szobaszam, datum, ar):
        self.szobaszam = szobaszam
        self.datum = datum
        self.ar = ar

# Foglalas kezelő osztály
class FoglalasKezelo:
    def __init__(self, szalloda):
        self.szalloda = szalloda
        self.foglalasok = []

    def foglalas(self, datum_str, szoba_tipusa):
        datum = datetime.strptime(datum_str, '%Y-%m-%d').date()
        if datum <= date.today():
            print("A foglalás dátuma nem lehet a mai napnál korábbi.")
            return
        for szoba in self.szalloda.szobak:
            if szoba.szoba_tipusa() != szoba_tipusa:
                continue
            foglalt = any(foglalas.szobaszam == szoba.szobaszam and foglalas.datum == datum for foglalas in self.foglalasok)
            if not foglalt:
                foglalas = Foglalas(szoba.szobaszam, datum, szoba.ar)
                self.foglalasok.append(foglalas)
                print(f"Foglalás sikeresen létrehozva: Szobaszám {szoba.szobaszam}, Dátum: {datum_str}, Ár: {szoba.ar} Ft")
                return
        print("Sajnáljuk, nincsenek elérhető szobák ezen a dátumon.")

    def lemondas(self, szobaszam, datum_str):
        datum = datetime.strptime(datum_str, '%Y-%m-%d').date()
        for foglalas in self.foglalasok:
            if foglalas.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                print("Foglalás sikeresen lemondva.")
                return True
        print("Nem található ilyen foglalás.")
        return False

    def foglalasok_listazasa(self):
        if not self.foglalasok:
            print("Nincsenek foglalások.")
            return
        for foglalas in self.foglalasok:
            print(f"Szobaszám: {foglalas.szobaszam}, Dátum: {foglalas.datum.strftime('%Y-%m-%d')}, Ár: {foglalas.ar} Ft")

# Felhasználói interfész
def felhasznaloi_interfesz(szalloda):
    foglalas_kezelo = FoglalasKezelo(szalloda)
    while True:
        print("\nVálasszon az alábbi opciók közül:")
        print("1. Foglalás")
        print("2. Lemondás")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Adja meg a választott opció számát: ")
        if valasztas == "1":
            szoba_tipusa = input("Egyágyas vagy kétágyas szobát szeretne foglalni? (egyágyas/kétágyas): ").strip()
            datum = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
            foglalas_kezelo.foglalas(datum, szoba_tipusa)
        elif valasztas == "2":
            szobaszam = input("Adja meg a szobaszámot, amelyik foglalást le szeretné mondani: ")
            datum = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
            foglalas_kezelo.lemondas(szobaszam, datum)
        elif valasztas == "3":
            foglalas_kezelo.foglalasok_listazasa()
        elif valasztas == "4":
            print("Köszönjük, hogy használta a Szálloda Foglalási Rendszerünket!")
            break
        else:
            print("Érvénytelen választás. Kérjük, próbálja újra.")

# Példa adatokkal való inicializálás
def rendszer_inicializalasa():
    szalloda = Szalloda("Példa Szálloda")
    szalloda.szoba_hozzaadasa(EgyagyasSzoba(10000, "101"))
    szalloda.szoba_hozzaadasa(KetagyasSzoba(15000, "102"))
    szalloda.szoba_hozzaadasa(EgyagyasSzoba(10000, "103"))
    return szalloda

if __name__ == "__main__":
    szalloda = rendszer_inicializalasa()
    felhasznaloi_interfesz(szalloda)
