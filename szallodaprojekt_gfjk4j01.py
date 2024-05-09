from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class Szoba(ABC):
    def __init__(self, szobaszam):
        self.szobaszam = szobaszam

    @abstractmethod
    def ar_szamolas(self, napok):
        pass

class EgyagyasSzoba(Szoba):
    def ar_szamolas(self, napok):
        return 10000 * napok

class KetagyasSzoba(Szoba):
    def ar_szamolas(self, napok):
        return 15000 * napok

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def SzobaAdd(self, szoba):
        self.szobak.append(szoba)

    def SzobaListaz(self):
        for szoba in self.szobak:
            print(f"Szobaszám: {szoba.szobaszam}")

class Foglalas:
    def __init__(self, szoba, datum, napok):
        self.szoba = szoba
        self.datum = datum
        self.napok = napok

class FoglalasKezelo:
    def __init__(self, szalloda):
        self.szalloda = szalloda
        self.foglalasok = []

    def Foglalas(self, szobaszam, datum, napok):
        for szoba in self.szalloda.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas_datum = datetime.combine(datum, datetime.min.time())
                if foglalas_datum < datetime.now():
                    print("Csak jövőbeni foglalás lehetséges.")
                    return None
                for foglalas in self.foglalasok:
                    if foglalas.szoba == szoba and (foglalas.datum==datum or datum_interval(datum,datum+timedelta(days=napok),foglalas.datum,foglalas.datum+timedelta(days=foglalas.napok))):
                        print("A megadott dátumra ("+str(datum)+ ") már foglalt a " + szobaszam + " számú szoba.")
                        return None

                foglalas = Foglalas(szoba, datum, napok)
                self.foglalasok.append(foglalas)
                return szoba.ar_szamolas(napok)
        print("Nem létező szobaszám.")
        return None

    def FoglalasLemond(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            print("Foglalás sikeresen törölve.")
        else:
            print("Nincs ilyen foglalás.")

    def FoglalasListaz(self):
        for foglalas in self.foglalasok:
            print(f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}, Napok: {foglalas.napok}")

def SzallodaLetrehozas():
    szalloda = Szalloda("Hotel GDF")
    szalloda.SzobaAdd(EgyagyasSzoba("101"))
    szalloda.SzobaAdd(EgyagyasSzoba("102"))
    szalloda.SzobaAdd(KetagyasSzoba("201"))
    return szalloda
def datum_interval(datum1_kezdet, datum1_veg, datum2_kezdet, datum2_veg):
    return (datum1_kezdet <= datum2_veg and datum1_veg >= datum2_kezdet) or \
           (datum2_kezdet <= datum1_veg and datum2_veg >= datum1_kezdet)
def main():
    szalloda = SzallodaLetrehozas()
    foglalas_kezelo = FoglalasKezelo(szalloda)

    # Példa foglalások hozzáadása
    foglalas_kezelo.Foglalas("101", datetime(2024, 7, 1), 3)
    foglalas_kezelo.Foglalas("102", datetime(2024, 6, 2), 2)
    foglalas_kezelo.Foglalas("201", datetime(2024, 8, 3), 5)
    foglalas_kezelo.Foglalas("101", datetime(2024, 8, 4), 1)
    foglalas_kezelo.Foglalas("102", datetime(2024, 7, 5), 4)

    # Felhasználói interfész
    while True:
        print("\nVálassz egy műveletet:")
        print("1. Szoba foglalás")
        print("2. Foglalás lemondás")
        print("3. Foglalások listázása")
        print("4. Szobák listázása")
        print("5. Kilépés")
        valasztas = input("Művelet kiválasztása (1/2/3/4/5): ")

        if valasztas == "1":
            szobaszam = input("Adja meg a foglalni kívánt szoba számát: ")
            datum = datetime.strptime(input("Adja meg a foglalás dátumát (YYYY-MM-DD): "), "%Y-%m-%d")
            napok = int(input("Adja meg a foglalás napjainak számát: "))
            ar = foglalas_kezelo.Foglalas(szobaszam, datum, napok)
            if ar:
                print(f"A foglalás sikeres. Ár: {ar}")
            else:
                print("Nem sikerült foglalni a szobát.")

        elif valasztas == "2":
            print("Kérem add meg a lemondani kívánt foglalás adatait:")
            szobaszam = input("Szoba száma: ")
            datum = datetime.strptime(input("Foglalás dátuma (YYYY-MM-DD): "), "%Y-%m-%d")
            for foglalas in foglalas_kezelo.foglalasok:
                if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                    foglalas_kezelo.FoglalasLemond(foglalas)
                    break

        elif valasztas == "3":
            print("Összes foglalás:")
            foglalas_kezelo.FoglalasListaz()
        elif valasztas == "4":
            print("Szobák:")
            szalloda.SzobaListaz()

        elif valasztas == "5":
            print("Kilépés...")
            break

        else:
            print("Érvénytelen választás. Kérem válasszon a felsorolt lehetőségek közül.")

if __name__ == "__main__":
    main()