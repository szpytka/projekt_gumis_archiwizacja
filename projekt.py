import uuid
import pickle

from datetime import datetime, timedelta


class Dokument:
    def __init__(self, tytul, rok, kategoria, miejsce_przechowywania, liczba_egz):
        self.uuid = uuid.uuid4()  # Generowanie unikalnego identyfikatora
        self.tytul = tytul
        self.rok = rok
        self.kategoria = kategoria
        self.miejsce_przechowywania = miejsce_przechowywania
        self.liczba_egz = liczba_egz
        self.historia_zmian = []
        self.wypozyczenia = []

    def dodaj_historie_zmian(self, user, akcja):
        self.historia_zmian.append({
            'user': user,
            'akcja': akcja,
            'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def dodaj_wypozyczenie(self, user):
        data_wypozyczenia = datetime.now()
        przewidywana_data_powrotu = data_wypozyczenia + timedelta(days=14)
        self.wypozyczenia.append({
            'user': user,
            'data_wypozyczenia': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'przewidywana_data_powrotu': przewidywana_data_powrotu.strftime("%Y-%m-%d %H:%M:%S"),
            'data_zwrotu': None
        })

    def zakoncz_wypozyczenie(self):
        if self.wypozyczenia and self.wypozyczenia[-1]['data_zwrotu'] is None:
            self.wypozyczenia[-1]['data_zwrotu'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Archiwum:
    def __init__(self, nazwa_pliku):
        self.nazwa_pliku = nazwa_pliku
        self.dokumenty = self.wczytaj_z_pliku()

    def zapisz_do_pliku(self):
        with open(self.nazwa_pliku, 'wb') as plik:
            pickle.dump(self.dokumenty, plik)

    def wczytaj_z_pliku(self):
        try:
            with open(self.nazwa_pliku, 'rb') as plik:
                return pickle.load(plik)
        except FileNotFoundError:
            return []

    def dodaj_dokument(self, dokument, user):
        dokument.dodaj_historie_zmian(user, "Dodanie dokumentu")
        self.dokumenty.append(dokument)
        self.zapisz_do_pliku()
        print(f"\nDodano dokument do archiwum. UUID: {dokument.uuid}")

    def usun_dokument(self, uuid, user):
        for dokument in self.dokumenty:
            if str(dokument.uuid) == uuid:
                dokument.dodaj_historie_zmian(user, "Usunięcie dokumentu")
                self.dokumenty.remove(dokument)
                self.zapisz_do_pliku()
                print("Usunięto dokument z archiwum.")
                return
        print("Nie znaleziono dokumentu o podanym UUID.")

    def modyfikuj_dokument(self, uuid, nowy_tytul, nowy_rok, nowa_kategoria, nowe_miejsce_przechowywania,
                           nowa_liczba_egz, user):
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
                dokument.dodaj_historie_zmian(user, "Modyfikacja dokumentu")
                self.zapisz_do_pliku()
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

    def pokaz_dokumenty(self):
        if not self.dokumenty:
            print("Brak dokumentów w archiwum")
        else:
            print("Wszystkie dokumenty w archiwum:")
            for dokument in self.dokumenty:
                print(f"\nUUID: {dokument.uuid}")
                print(
                    f"Tytuł: {dokument.tytul}, Rok: {dokument.rok}, Kategoria: {dokument.kategoria}, Miejsce Przechowanywania: {dokument.miejsce_przechowywania}, Liczba egzemplarzy: {dokument.liczba_egz} ")

    def wypozycz_dokument(self, uuid, user):
        for dokument in self.dokumenty:
            if str(dokument.uuid) == uuid:
                if dokument.liczba_egz > 0:
                    dokument.liczba_egz -= 1
                    dokument.dodaj_wypozyczenie(user)
                    dokument.dodaj_historie_zmian(user, "Wypożyczenie dokumentu")
                    self.zapisz_do_pliku()
                    print("Dokument został wypożyczony.")
                else:
                    print("Brak dostępnych egzemplarzy do wypożyczenia.")
                return
        print("Podane UUID nie istnieje w archiwum.")

    def zwroc_dokument(self, uuid, user):
        for dokument in self.dokumenty:
            if str(dokument.uuid) == uuid:
                dokument.zakoncz_wypozyczenie()
                dokument.liczba_egz += 1
                dokument.dodaj_historie_zmian(user, "Zwrot dokumentu")
                self.zapisz_do_pliku()
                print("Dokument został zwrócony.")
                return
        print("Podane UUID nie istnieje w archiwum.")

    def pokaz_historie(self, uuid):
        for dokument in self.dokumenty:
            if str(dokument.uuid) == uuid:
                print(f"Historia zmian dla dokumentu {dokument.tytul} (UUID: {dokument.uuid}):")
                for wpis in dokument.historia_zmian:
                    print(f"Data: {wpis['data']}, Użytkownik: {wpis['user']}, Akcja: {wpis['akcja']}")
                print("\nWypożyczenia:")
                for wypozyczenie in dokument.wypozyczenia:
                    print(
                        f"Użytkownik: {wypozyczenie['user']}, Data wypożyczenia: {wypozyczenie['data_wypozyczenia']}, Data zwrotu: {wypozyczenie['data_zwrotu']}")
                return
        print("Podane UUID nie istnieje w archiwum.")

    def pokaz_aktywne_wypozyczenia(self):
        aktywne_wypozyczenia = []
        for dokument in self.dokumenty:
            for wypozyczenie in dokument.wypozyczenia:
                if wypozyczenie['data_zwrotu'] is None:
                    aktywne_wypozyczenia.append({
                        'uuid': dokument.uuid,
                        'tytul': dokument.tytul,
                        'user': wypozyczenie['user'],
                        'data_wypozyczenia': wypozyczenie['data_wypozyczenia'],
                        'przewidywana_data_powrotu': wypozyczenie['przewidywana_data_powrotu']
                    })
        if aktywne_wypozyczenia:
            print("Aktywne wypożyczenia:")
            for wypozyczenie in aktywne_wypozyczenia:
                print(f"UUID: {wypozyczenie['uuid']}")
                print(f"Tytuł: {wypozyczenie['tytul']}")
                print(f"Użytkownik: {wypozyczenie['user']}")
                print(f"Data wypożyczenia: {wypozyczenie['data_wypozyczenia']}")
                print(f"Przewidywana data powrotu: {wypozyczenie['przewidywana_data_powrotu']}")
                print("---------------------------")
        else:
            print("Brak aktywnych wypożyczeń.")


class UserManager:
    def __init__(self, nazwa_pliku):
        self.nazwa_pliku = nazwa_pliku
        self.users = self.wczytaj_z_pliku()

    def zapisz_do_pliku(self):
        with open(self.nazwa_pliku, 'wb') as plik:
            pickle.dump(self.users, plik)

    def wczytaj_z_pliku(self):
        try:
            with open(self.nazwa_pliku, 'rb') as plik:
                return pickle.load(plik)
        except FileNotFoundError:
            return ['Knap', 'Szpytka', 'Admin']

    def pokaz_uzytkownikow(self):
        print("Lista użytkowników:")
        for user in self.users:
            print(user)

    def dodaj_uzytkownika(self, nazwa_uzytkownika):
        if nazwa_uzytkownika in self.users:
            print("Użytkownik już istnieje.")
        else:
            self.users.append(nazwa_uzytkownika)
            self.zapisz_do_pliku()
            print(f"Dodano nowego użytkownika: {nazwa_uzytkownika}")


def main():
    print("Witaj w systemie archiwizacji dokumentów!")

    nazwa_pliku = 'archiwum.pkl'
    nazwa_pliku_uzytkownicy = 'users.pkl'
    archiwum = Archiwum(nazwa_pliku)
    user_manager = UserManager(nazwa_pliku_uzytkownicy)

    user = input("Podaj nazwę użytkownika: ")

    if user not in user_manager.users:
        print("Niepoprawna nazwa użytkownika.")
        return []

    print(f"Witaj, {user}!")

    while True:
        print("\nWybierz jedną z dostępnych opcji:")

        print("-----Dokumenty-----")
        print("1. Dodaj nowy dokument do archiwum")
        print("2. Usuń dokument z archiwum")
        print("3. Zaktualizuj informacje o dokumencie")
        print("4. Pokaż wszystkie dokumenty")
        print("5. Pokaż historię dokumentu")

        print("-----Wypożyczanie-----")
        print("6. Wypożycz dokument")
        print("7. Zwróć dokument")
        print("8. Pokaż aktywne wypożyczenia")

        print("-----Użytkownicy-----")
        print("9. Dodaj nowego użytkownika")
        print("10. Pokaż wszystkich użytkowników")

        print("-----Wyszukiwanie-----")
        print("11. Szukaj dokumentu")

        print("12. Wyjście\n")

        choice = input("Wybierz numer opcji: ")

        if choice == "1":
            tytul = input("Podaj tytuł dokumentu: ")
            rok = input("Podaj rok dokumentu: ")
            kategoria = input("Podaj kategorię dokumentu: ")
            miejsce_przechowywania = input("Podaj miejsce przechowywania dokumentu: ")
            liczba_egz = int(input("Podaj liczbę egzemplarzy dokumentu: "))
            dokument = Dokument(tytul, rok, kategoria, miejsce_przechowywania, liczba_egz)
            archiwum.dodaj_dokument(dokument, user)

        elif choice == "2":
            uuid_do_usuniecia = input("Podaj UUID dokumentu do usunięcia: ")
            archiwum.usun_dokument(uuid_do_usuniecia, user)

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
                                        nowe_miejsce_przechowywania, nowa_liczba_egz, user)
        elif choice == "4":
            archiwum.pokaz_dokumenty()

        elif choice == "5":
            uuid_do_historia = input("Podaj UUID dokumentu, aby zobaczyć jego historię: ")
            archiwum.pokaz_historie(uuid_do_historia)

        elif choice == "6":
            uuid_do_wypozyczenia = input("Podaj UUID dokumentu do wypożyczenia: ")
            archiwum.wypozycz_dokument(uuid_do_wypozyczenia, user)

        elif choice == "7":
            uuid_do_zwrotu = input("Podaj UUID dokumentu do zwrotu: ")
            archiwum.zwroc_dokument(uuid_do_zwrotu, user)

        elif choice == "8":
            archiwum.pokaz_aktywne_wypozyczenia()

        elif choice == "9":
            nowy_uzytkownik = input("Podaj nazwę nowego użytkownika: ")
            user_manager.dodaj_uzytkownika(nowy_uzytkownik)

        elif choice == "10":
            user_manager.pokaz_uzytkownikow()

        elif choice == "11":
            parametr_szukania = input("Podaj tytuł, rok lub miejsce przechowywania dokumentu: ")
            archiwum.szukaj_dokumentu(parametr_szukania)



        elif choice == "12":
            print("Dziękujemy za skorzystanie z systemu archiwizacji dokumentów. Do widzenia!")
            break
        else:
            print("\nNiepoprawny wybór. Spróbuj ponownie.")


# Jeśli skrypt jest importowany jako moduł, blok ten nie zostanie wykonany, ponieważ zmienna __name__ przyjmuje wartość "__main__" w głównym pliku
if __name__ == "__main__":
    main()
    input("Naciśnij Enter, aby zakończyć...")
