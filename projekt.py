import uuid

class Dokument:
    def __init__(self, tytul, rok, kategoria, miejsce_przechowywania, liczba_egz):
        self.uuid = uuid.uuid4()  # Generowanie unikalnego identyfikatora
        self.tytul = tytul
        self.rok = rok
        self.kategoria = kategoria
        self.miejsce_przechowywania = miejsce_przechowywania
        self.liczba_egz = liczba_egz

class Archiwum:
    def __init__(self):
        self.dokumenty = []

    def dodaj_dokument(self, dokument):
        self.dokumenty.append(dokument)
        print(f"\nDodano dokument do archiwum. UUID: {dokument.uuid}")

    def usun_dokument(self, uuid):
        for dokument in self.dokumenty:
            if str(dokument.uuid) == uuid:
                self.dokumenty.remove(dokument)
                print("Usunięto dokument z archiwum.")
                return
        print("Nie znaleziono dokumentu o podanym UUID.")

    def modyfikuj_dokument(self, uuid, nowy_tytul, nowy_rok, nowa_kategoria, nowe_miejsce_przechowywania,
                           nowa_liczba_egz):
        if uuid not in [str(dokument.uuid) for dokument in self.dokumenty]:
            print("Podane UUID nie istnieje w archiwum.")
            return

        for dokument in self.dokumenty:
            if str(dokument.uuid) == uuid:
                dokument.tytul = nowy_tytul
                dokument.rok = nowy_rok
                dokument.kategoria = nowa_kategoria
                dokument.miejsce_przechowywania = nowe_miejsce_przechowywania
                dokument.liczba_egz = nowa_liczba_egz
                print("Dokument został zaktualizowany.")
                return

    def szukaj_dokumentu(self, parametr_szukania):
        znalezione_dokumenty = []
        for dokument in self.dokumenty:
            if parametr_szukania.lower() in [dokument.tytul.lower(), str(dokument.rok),
                                             dokument.miejsce_przechowywania.lower()]:
                znalezione_dokumenty.append(dokument)
        if znalezione_dokumenty:
            print("Znalezione dokumenty:")
            for dokument in znalezione_dokumenty:
                print(f"\nUUID: {dokument.uuid}")
                print(
                    f"Tytuł: {dokument.tytul}, Rok: {dokument.rok}, Kategoria: {dokument.kategoria}, Miejsce przechowywania: {dokument.miejsce_przechowywania}, Liczba egzemplarzy: {dokument.liczba_egz}")
        else:
            print("Brak dokumentów pasujących do podanych kryteriów.")


def main():
    print("Witaj w systemie archiwizacji dokumentów!")

    archiwum = Archiwum()

    while True:
        print("\nWybierz jedną z dostępnych opcji:")
        print("1. Dodaj nowy dokument do archiwum")
        print("2. Usuń dokument z archiwum")
        print("3. Zaktualizuj informacje o dokumencie")
        print("4. Szukaj dokumentu")
        print("5. Wyjście\n")

        choice = input("Wybierz numer opcji: ")

        if choice == "1":
            tytul = input("Podaj tytuł dokumentu: ")
            rok = input("Podaj rok dokumentu: ")
            kategoria = input("Podaj kategorię dokumentu: ")
            miejsce_przechowywania = input("Podaj miejsce przechowywania dokumentu: ")
            liczba_egz = input("Podaj liczbę egzemplarzy dokumentu: ")
            dokument = Dokument(tytul, rok, kategoria, miejsce_przechowywania, liczba_egz)
            archiwum.dodaj_dokument(dokument)
        elif choice == "2":
            uuid_do_usuniecia = input("Podaj UUID dokumentu do usunięcia: ")
            archiwum.usun_dokument(uuid_do_usuniecia)
        elif choice == "3":
            uuid_do_modyfikacji = input("Podaj UUID dokumentu do zaktualizowania: ")
            if not uuid_do_modyfikacji:
                print("Nie podano UUID dokumentu.")
                continue

            dostepne_uuid = [str(dokument.uuid) for dokument in archiwum.dokumenty]
            if uuid_do_modyfikacji not in dostepne_uuid:
                print("Podane UUID nie istnieje w archiwum.")
                continue

            nowy_tytul = input("Podaj nowy tytuł dokumentu: ")
            nowy_rok = input("Podaj nowy rok dokumentu: ")
            nowa_kategoria = input("Podaj nową kategorię dokumentu: ")
            nowe_miejsce_przechowywania = input("Podaj nowe miejsce przechowywania dokumentu: ")
            nowa_liczba_egz = input("Podaj nową liczbę egzemplarzy dokumentu: ")

            archiwum.modyfikuj_dokument(uuid_do_modyfikacji, nowy_tytul, nowy_rok, nowa_kategoria,
                                        nowe_miejsce_przechowywania, nowa_liczba_egz)
        elif choice == "4":
            parametr_szukania = input("Podaj tytuł, rok lub miejsce przechowywania dokumentu: ")
            archiwum.szukaj_dokumentu(parametr_szukania)
        elif choice == "5":
            print("Dziękujemy za skorzystanie z systemu archiwizacji dokumentów. Do widzenia!")
            break
        else:
            print("\nNiepoprawny wybór. Spróbuj ponownie.")

if __name__ == "__main__":
    main()
    input("Naciśnij Enter, aby zakończyć...")