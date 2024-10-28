from colorama import init
from termcolor import colored
from random import choice
from csv import reader
from bs4 import BeautifulSoup
import pyfiglet
import requests

init()

ascii_art = pyfiglet.figlet_format("Guess The Quote")
colored_ascii = colored(ascii_art, color='green')
print(colored_ascii)

BASE_URL = 'https://quotes.toscrape.com/'

all_quotes = []
with open('quotes.csv') as file:
    csv_reader = reader(file)
    for row in csv_reader:
        all_quotes.append(row)

for quote in all_quotes:
    if not quote:
        all_quotes.remove(quote)


def start_game():
    random_quote = choice(all_quotes) 
    text = random_quote[0]
    author = random_quote[1].lower()
    bio_link = random_quote[2]
    tries = 4

    print(f"{text}")
    anwser = ""
    while anwser != author and tries > 0:
        anwser = input(
            f'Can you guess who\'d said that? You got {tries} tries!\n').lower()
        if anwser == author:
            print('Correct! You won!')
            break
        tries -= 1
        if tries == 3:
            response = requests.get(f'{BASE_URL}{bio_link}')
            soup = BeautifulSoup(response.text, "html.parser")
            birth_date = soup.find(class_='author-born-date').get_text()
            birth_location = soup.find(
                class_='author-born-location').get_text()
            print(
                f'Let me give you a hint!\nThis person was born on {birth_date} {birth_location}.')
        elif tries == 2:
            print(
                f'Here\'s another hint. This person name starts with {
                    author[0].upper()}'
                )
        elif tries == 1:
            lastname = author.split(" ")[1][0]
            print(
                f'Here\'s the last hint. This person last name starts with {
                    lastname.upper()}'
                )
        else:
            print(f'You ran out of tries :(\nThe answer was {author}')

    play_again = ''
    while play_again not in ('y', 'n'):
        play_again = input('Do you want to play again (y/n)?\n')

    if play_again.lower() == 'y':
        start_game()
    else:
        print('Bye! :)')


start_game()
