from disease import Disease
from files import read_meetings_csv

def main():
    people = read_meetings_csv('example_data/meetings.csv')
    covid = Disease("covid", 100)
    print(people['Dexter Thomas'].who_is_infected(covid))

if __name__ == "__main__":
    main()