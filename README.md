# Podział programu na klasy i opis klas

## Person

Klasa przechowuje podstawowe informacje na temat danego człowieka (Imię i nazwisko) oraz listę spotkań, w których brał udział (obiekty klasy Meeting). Za pomocą jej metod możemy dodawać nowe spotkania (podając osobę, z którą się spotkała, ich datę (format ISO 8601) i czas trwania w minutach) lub je usuwać (podając ich UUID), np. w przypadku, gdy zrobiliśmy błąd przy wprowadzaniu danych, lecz najistotniejszą metodą jest who_is_infected, która pozwala nam wskazać obecną osobę jako zakażoną, i podając datę wykrycia zarażenia i chorobę, typuje nam listę potencjalnie zakażonych osób.

## Meeting

Klasa jest używana do przechowywania informacji o danym spotkaniu. Przy inicjalizacji obiektu tej klasy, generowany jest unikatowy identyfikator spotkania, a jej pola składają się z 2 osób biorących udział w spotkaniu, daty (format ISO 8601) oraz czasu trwania spotkania w minutach.

## Disease

Klasa przechowuje dane dotyczących choroby, jej nazwę oraz okres zaraźliwości w minutach. Obiekty tej klasy są używane do wyznaczania osób zakażonych.

## TUI_UI

Nazwa to skrót od Text-based user interface. Klasa odpowiada za konsolowy interfejs użytkownika. Za pomocą jego metod możemy:

- Dodać spotkanie do bazy spotkań
- Usunąć spotkanie z bazy spotkań
- Sprawdzić listę spotkań w bazie spotkań - Dodać chorobę do bazy chorób
- Usunąć chorobę z bazy chorób
- Sprawdzić listę chorób w bazie chorób
- Wskazać osobę zakażoną i na podstawie listy dodanych spotkań uzyskać listę potencjalnie zakażonych osób
- Zaimportować listę spotkań z pliku .csv do bazy spotkań - Zakończyć działanie programu

## CLI_UI

Nazwa to skrót od Command-line interface. Klasa odpowiada za interfejs wiersza poleceń. Za jego pomocą możemy podać ścieżkę do pliku .csv, imię i nazwisko osoby zakażonej, czas zaraźliwości choroby oraz datę zdiagnozowania choroby u tej osoby (format ISO 8601). Opcjonalnymi argumentami są _—name_ (nazwa choroby) i _—output <nazwa_pliku>_ (zapisywanie wyniku w postaci listy osób potencjalnie zakażonych do pliku).

# Instrukcja użytkowania

## 1. Tekstowy interfejs użytkownika

Program możemy uruchomić za pomocą polecenia:
`python3 ./infection_tracker.py`
W konsoli pojawia się nam interfejs, który wygląda w następujący sposób:
Wybieramy opcje wpisując numer od 1 do 9.

###### 1. Spotkania

Wybierając opcję nr 1 musimy podać:

- Imię pierwszej osoby biorącej udział w spotkaniu
- Nazwisko pierwszej osoby biorącej udział w spotkaniu - Imię drugiej osoby biorącej udział w spotkaniu
- Nazwisko drugiej osoby biorącej udział w spotkaniu
- Dokładną datę spotkania w formacie ISO 8601
- Czas trwania spotkania w minutach
  Po dodaniu spotkania zostajemy przeniesieni ponownie do menu głównego. Wybierając opcję nr 3 możemy sprawdzić listę spotkań w naszej bazie.

Wybierając opcję nr 2 możemy usunąć dodane przez nas spotkanie podając jego UUID. Wpisując niepoprawne UUID, program przeszuka bazę spotkań, ale nic nie zostanie usunięte.
Nasza baza jest teraz pusta.

###### 2. Choroby

Wybierając opcję nr 4 możemy dodać chorobę podając kolejno jej nazwę i okres zaraźliwości w minutach.
Możemy teraz sprawdzić bazę chorób wybierając opcję nr 6.
Choroby usuwamy za pomocą opcji nr 5 podając jej numer indeksu.

###### 3. Pliki csv i lista potencjalnie zakażonych.

Plik .csv musi mieć następujące kolumny:
**Name_1, Surname_1, Name_2, Surname_2, Date, Duration**

- Imię pierwszej osoby biorącej udział w spotkaniu
- Nazwisko pierwszej osoby biorącej udział w spotkaniu - Imię drugiej osoby biorącej udział w spotkaniu
- Nazwisko drugiej osoby biorącej udział w spotkaniu
- Dokładną datę spotkania w formacie ISO 8601
- Czas trwania spotkania w minutach

W folderze tests/example_data znajduje się przykładowy arkusz .csv ze spotkaniami, który możemy użyć do testowania reszty funkcji programu. W tym celu zaimportujemy go wybierając opcję nr 8.
Za pomocą opcji nr 3 możemy sprawdzić czy spotkania zaimportowały się pomyślnie.
Aby wskazać listę osób potencjalnie zakażonych, musimy najpierw stworzyć chorobę, tak jak w podpunkcie 2.
Teraz możemy wybrać opcję nr 7. Kolejno podajemy imię i nazwisko osoby zakażonej, datę zdiagnozowania u niego choroby w formacie ISO 8601 i numer indeksu choroby.
Zwrócona zostanie lista potencjalnie zakażonych osób.

## 2. Interfejs wiersza poleceń

Program przyjmuje następujące parametry:
meetings - plik .csv z listą spotkań
infected - imię i nazwisko osoby zakażonej
period - okres zaraźliwości choroby w minutach
date - data zdiagnozowania choroby u osoby w formacie ISO 8601 I opcjonalne parametry:
—name NAME - nazwa choroby
—output [OUTPUT] - zapisywanie wyniku programu do danego pliku

Plik .csv musi mieć następujące kolumny:
**Name_1, Surname_1, Name_2, Surname_2, Date, Duration**

- Imię pierwszej osoby biorącej udział w spotkaniu
- Nazwisko pierwszej osoby biorącej udział w spotkaniu - Imię drugiej osoby biorącej udział w spotkaniu
- Nazwisko drugiej osoby biorącej udział w spotkaniu
- Dokładną datę spotkania w formacie ISO 8601
- Czas trwania spotkania w minutach
  W wierszach muszą się znaleźć kolejno:

###### Przykład nr 1

Przykładowe polecenie biorące listę spotkań z pliku meetings.csv, wskazujące Audrey Brooks jako osobę zakażoną dnia 2021-12-02 o godzinie 12:00 chorobą z okresem zaraźliwości wynoszącym 12000 minut.

`python3 ./infection_tracker.py tests/example_data/meetings.csv 'Audrey Brooks'`

Wynikiem jest:
_12000 '2021-12-02 12:00'_
_Tess Spencer, Savana Wells, Camila Evans, Owen Nelson, Andrew Cole, Audrey Brooks, Jenna Payne, Eddy Morrison, Grace Andrews, Albert Spencer, Marcus Moore, Haris Thompson_

###### Przykład nr 2

`python3 ./infection_tracker.py tests/example_data/meetings.csv 'Mike Jones' 2000 '2021-12-01 01:00' --output list.txt`
Wynikiem jest:
_Haris Thompson, James Johnston, Mike Jones_
Dodatkowo utworzony zostaje plik list.txt z powyższym wynikiem.
