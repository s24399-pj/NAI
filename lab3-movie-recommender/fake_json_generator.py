import json
import random

film_titles = [
    "Incepcja", "Matrix", "Forrest Gump", "Skazani na Shawshank", "Interstellar",
    "Fight Club", "Pulp Fiction", "Zielona Mila", "Gladiator", "Ojciec Chrzestny",
    "Władca Pierścieni", "Django", "Gran Torino", "Avatar", "Shrek",
    "Harry Potter", "Gwiezdne Wojny", "Jurassic Park", "Titanic", "Piękny Umysł",
    "Mad Max: Na drodze gniewu", "Batman: Początek", "Iron Man", "Deadpool",
    "Kapitan Ameryka", "Thor", "Avengers", "Spider-Man", "Strażnicy Galaktyki",
    "Ant-Man", "Czarna Pantera", "Doktor Strange", "Kapitan Marvel", "Aquaman",
    "Wonder Woman", "Liga Sprawiedliwości", "Suicide Squad", "Joker", "Logan",
    "Szybcy i Wściekli", "John Wick", "Mission Impossible", "James Bond",
    "Blade Runner", "E.T.", "Obcy", "Terminator", "Rocky", "Rambo",
    "Szeregowiec Ryan", "Szklana Pułapka", "Polowanie na Czerwony Październik",
    "Bękarty Wojny", "Infiltracja", "Wilk z Wall Street", "Lot nad kukułczym gniazdem",
    "Mechaniczna Pomarańcza", "Lśnienie", "Full Metal Jacket", "Requiem dla snu",
    "Trainspotting", "Podziemny Krąg", "American Beauty", "Whiplash", "La La Land",
    "The Social Network", "Człowiek z Blizną", "Chłopcy z Ferajny",
    "Psychoza", "Milczenie Owiec", "Se7en", "Memento", "Wyspa Tajemnic",
    "Blade Runner 2049", "Her", "Czarne Lustro", "Narcos", "Breaking Bad",
    "Gra o Tron", "Westworld", "Stranger Things", "The Crown", "Dark",
    "Wiedźmin", "Rick i Morty", "BoJack Horseman", "Peaky Blinders",
    "Dom z Papieru", "Sherlock", "True Detective", "Fargo", "Mindhunter",
    "Ozark", "Better Call Saul", "The Mandalorian", "Lupin", "Sukcesja"
]

first_names = [
    "Jan", "Anna", "Piotr", "Maria", "Krzysztof", "Katarzyna", "Andrzej",
    "Małgorzata", "Tomasz", "Agnieszka", "Paweł", "Barbara", "Jacek",
    "Ewa", "Michał", "Elżbieta", "Marcin", "Magdalena", "Jakub", "Joanna",
    "Adam", "Aleksandra", "Łukasz", "Monika", "Grzegorz", "Paulina",
    "Dawid", "Karolina", "Mateusz", "Beata", "Marek", "Dorota", "Dariusz",
    "Justyna", "Wojciech", "Natalia", "Maciej", "Iwona", "Szymon", "Ewelina"
]

last_names = [
    "Kowalski", "Nowak", "Wiśniewski", "Wójcik", "Kowalczyk", "Kamiński",
    "Lewandowski", "Zieliński", "Szymański", "Woźniak", "Dąbrowski",
    "Kozłowski", "Jankowski", "Mazur", "Wojciechowski", "Kwiatkowski",
    "Krawczyk", "Kaczmarek", "Piotrowski", "Grabowski", "Zając", "Pawłowski",
    "Michalski", "Król", "Wieczorek", "Jabłoński", "Wróbel", "Nowakowski",
    "Majewski", "Olszewski", "Stępień", "Malinowski", "Jaworski", "Adamczyk",
    "Dudek", "Nowicki", "Pawlak", "Górski", "Witkowski", "Walczak"
]

def generate_user_films(num_films):
    films = random.sample(film_titles, num_films)
    return [{"film": film, "ocena": random.randint(1, 10)} for film in films]

def generate_full_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

data = {"Osoby": []}
num_users = 12

for _ in range(num_users):
    num_films = random.randint(10, 20)
    user_name = generate_full_name()
    user_data = {
        "nazwa": user_name,
        "filmy": generate_user_films(num_films)
    }
    data["Osoby"].append(user_data)

with open('dane_filmy_2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Sztuczne dane zostały wygenerowane i zapisane do pliku dane_filmy_2.json")