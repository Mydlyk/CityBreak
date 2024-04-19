# Dokumentacja aplikacji „CityBreak”


## Opis uruchomienia Aplikacji
CityBreak został stworzony w pliku py w języku python z wykorzystaniem freameworka graficznego streamlit. Do uruchomiania aplikacji wymagane jest środowisko python(osobiście korzystałem z wersji pythona 3.12) oraz IDE obsługujące pliki pythonowe np. Visual Studio Code(z którego korzystałem). Do poprawnego działania aplikacji wymagane są następujące biblioteki:
langchain==0.1.16
langchain_core==0.1.43
python-decouple==3.8
Requests==2.31.0
streamlit==1.33.0
openai
Spis potrzebnych bibliotek znajduję się również w pliku „requirements.txt”.
W pliku .env znajdują się klucze potrzebne do poprawnego działania aplikacji.
Klucz Open_Api_Key z pozyskany https://openai.com/.
Login oraz hasło dla api DATAFORSEO pozyskane z https://app.dataforseo.com/
![image](https://github.com/Mydlyk/CityBreak/assets/65900710/47ffb084-5b05-482b-b82a-9ac2dd5e6088)

Aplikację uruchomiamy poprzez wykonanie polecenia  w terminalu:
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/00fb0a83-6efe-4e4e-8cfc-03caf8ddfee8)

Uruchomiona aplikacja powinna znajdować na adresie http://localhost:8501/
Opis uruchomienia Aplikacji Docker
Pierwszym krokiem jest zbudowanie obrazu z pliku Dockerfile. 
Przykładowa komenda budująca obraz:
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/ed448018-0280-4ec8-a585-d3fbb439e236)

docker build -f Dockerfile -t citybreak .
Następnym krokiem jest uruchomienie/stworzenie kontenera z obrazu.
 Przykładowe polecenie:
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/9fc1d8a2-b13c-4776-a85a-0baa4eb47f35)

docker run --name Citybreak -p 8501:8501 citybreak
Uruchomiona aplikacja powinna znajdować na adresie http://localhost:8501/.

## Opis działania aplikacji

Aplikacja jest chatem ze sztuczną inteligencją, która przeszukuje informacje o polskich miastach i odpowiada na pytanie jedynie związane z polskimi miastami w języku polskim. Chat utrzymuje również kontekst konwersacji i wypowiedzi.
Aplikacja po wysłaniu zapytania o miasto w Polsce za pomocą api DATAFORSEO przeszukuje internet w celu pozyskania informacji dla openai. Openai analizuje pozyskane dane, zadane pytanie, całkowity kontekst oraz stosuje się do zasad ustalonych w promp’cie. Gdy pytanie nie są jedoznacznym zapytaniem dla przeglądarki drugi llm analizuje je i na podstawie wcześniejszej historii i zwraca nowe pytania dla api DATAFORSEO(Przykład „Ilu ma mieszkańców” agent zwróci „Ile Lublin ma mieszkańców”). Gdy pytanie nie dotyczy polskiego miasta aplikacja odpowiada że nie jest to pytanie o polskie miasto.

## Opis kodu aplikacji
![image](https://github.com/Mydlyk/CityBreak/assets/65900710/d6612334-ce25-48f7-b1d9-a877d9747792)

Wykorzystanie kluczy api oraz zainicjalizowanie modelu sztucznej inteligencji temperatura oraz konkretny model openai które najlepiej odpowiadały to Temperatura=0 oraz model chat gpt 3.5-Turbo.
![image](https://github.com/Mydlyk/CityBreak/assets/65900710/7c89fde4-eb47-4367-80b3-134aae256930)
 
Stworzenie prompta dla llm’u w którym są ustalone zasady działania oraz przekazane są dane takie jak język, pytanie, kontekst, historia_chatu.
![image](https://github.com/Mydlyk/CityBreak/assets/65900710/77c29f4d-74f3-424f-9fbb-c4e748484533)

Stworzenie prompta dla pomocniczego llm tworzącego pytania dla DATAFORSEO jeśli pytanie jest zadane poprawnie nie zmienia go.
![image](https://github.com/Mydlyk/CityBreak/assets/65900710/b732af9f-13e0-4c86-a5fa-72a4a0eb5b84)
 
Utworzenie łańcucha przetwarzania.
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/1b28aa23-d55f-4b9a-93fe-cd8f6a12b876)

Funkcja generate_ai_response na podstawie st.session_state.chat_history(tutaj zapisywana jest historia chatu) tworzy historię chatu. Następnie pierwszy response odpowiada za dostosowania pytania do api. Zmienna json_wrapper przechowuje wyniki z wyszukiwanie w internecie przez DataForSeoAPIWrapper top_count oznacza górne 3 wyszukiwania, jso_results_fields okreśa jak dane zostały pobrane a w params ustawiona jest przeglądarka wyszukiwania.
Następnie Wywoływane jest wyszukiwanie i przypisane do zmiennej context.
Kolejny respone jest odpowiedzią chatu na zadane pytanie na podstawie kontekstu, pytania i historii. Funkcja zwraca wynik wyszukiwania w internecie i odpowiedz chatu, gdy coś pójdzie nie tak zwraca puste obiekty. 
![image](https://github.com/Mydlyk/CityBreak/assets/65900710/b9249f91-7ebe-4fcc-a7a2-64f1349212ad)

Chat do wpisywania pytań oraz tytuł aplikacji.
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/0ac8a42e-3274-49d6-a9d5-84231cf5d051)

Dodanie do historii chatu nowych odpowiedzi oraz zaznaczenie przez kogo została ona dodana.
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/9d3986ed-eb4c-4d80-a807-9366bfacba80)

Wyświetlenie powitania przez bota na początku konwersacji.
![image](https://github.com/Mydlyk/CityBreak/assets/65900710/8f4fb892-dce8-472a-be97-c2670d203b3d)
 
Ten kod odpowiada za wyświetlanie chatu.
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/a79a213c-0b42-44c9-8fb5-b7634d5c75ae)

Ten kod javascriptowy odpowiada za automatyczne scrolowanie w dół strony po dodaniu nowej wiadomości na wzór działania chatu gpt.

## Działanie aplikacji
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/d32c6232-63be-4f57-b073-c6dee035463a)

Rysunek 1 Ekran po uruchomieniu aplikacji
![image](https://github.com/Mydlyk/CityBreak/assets/65900710/2dc344d5-59cd-45b9-8d5b-a7070b1f52b3)
 
Rysunek 2 Zadanie pytania przez użytkownika oraz wyświetlenie z jakich stron chat pobrał dane 
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/3743dade-ab8b-4e9d-be69-22fa4cefb6f2)
 
Rysunek 3 Odpowiedz chatu na pytanie


 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/59021f5e-4b37-451f-8734-dd1e782ad3ff)

Rysunek 4 Zadanie pytanie podczas braku połączenia z Internetem
 ![image](https://github.com/Mydlyk/CityBreak/assets/65900710/a92701b7-0da8-4403-aacf-9a5a9436615d)
 
Rysunek 5 Odpowiedz na pytanie nie powiązane z polskimi miastami.
![image](https://github.com/Mydlyk/CityBreak/assets/65900710/55aec316-1d69-40e1-9030-1bab3504ff2d)
 
Rysunek 6 Pytania sprawdzające kontekst wypowiedzi
