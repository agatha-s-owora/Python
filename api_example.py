import requests

def main_menu():
    print("---------------------------------------")
    print("1 - Add pokemon")
    print("2 - View collection")
    print("3 - Exit program")
    print("---------------------------------------")
    response = input("Enter command: ").strip()
    while response < '1' or response > '3':
        response = input("Invalid - enter new command: ").strip()
    return response

def get_status_code(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    return requests.get(url)

def add_pokemon():
    pokemon_name = input("Pokemon name: ").strip().lower()
    response = get_status_code(pokemon_name)
    while response.status_code != 200:
        pokemon_name = input(f"Code: {response.status_code} Enter valid pokemon name: ").strip().lower()
        response = get_status_code(pokemon_name)
    return response.json()

def print_collection(pokemon_collection):
    for pokemon in pokemon_collection:
        print("------------------------------------------")
        print(f"ID: {pokemon["id"]}")
        print(f"Name: {pokemon["name"]}")
        print(f"Experience: {pokemon["base_experience"]}")
        print(f"Abilities: {pokemon["abilities"][0]["ability"]["url"]}")
        print("------------------------------------------")

def main():
    pokemon_collection = []

    menu_option = main_menu()
    while menu_option != '3':
        if menu_option == '1':
            pokemon = add_pokemon()
            pokemon_collection.append(pokemon)
            print("New pokemon added to collection")
        else:
            print_collection(pokemon_collection)
        menu_option = main_menu()

    print("End of program")


if __name__ == "__main__":
    main()
