from person import Person

example_contact_list = [
    {
        "person": Person("Ann", "Surreal"),
        "date": "21.12.2021",
        "hour": "12:24",
        "duration": "36"
    },
    {
        "person": Person("Brek", "Retter"),
        "date": "21.12.2021",
        "hour": "12:24",
        "duration": "36"
    }
]

example_infected_list = []

example_infected_list.append(example_contact_list[0]["person"])

person = Person("John", "William", example_contact_list)
print(example_infected_list[0] == example_contact_list[0]["person"])