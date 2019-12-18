# Adam Fernandes
# December 2019
# This program asks the user for movie specifications of the IMDB top 250 rated movies and prints a neat table.

from bs4 import BeautifulSoup
import requests as rq
import pandas as pd
import re

# Obtains user input for what year should be the marker for movie selection.
def get_year_threshold():
    print("---> What year should the films be Before / After? Input 'a' or 'b' and a four digit year (all one string). <---")
    correct_input = re.compile(r"(a|b)(\d{4})")
    ui = input()
    while (len(ui) != 5 or correct_input.match(ui) == None):
        print("---> Invalid input. Input 'a' (after) or 'b' (before) and a four digit year. <---")
        ui = input()
    if ui[0] == 'b':
        return ui[1:], True
    else:
        return ui[1:], False

# Obtains user input for what year should be the marker for movie selection.
def get_rating_threshold():
    print("---> What rating should the films be greater than or equal to [1-9.2]?. <---")
    ui = float(input())
    while ui < 1 or ui > 9.2:
        print("---> Invalid input. Rating must be between 1-9.2. <---")
        ui = float(input())
    return float(ui)

# Outputs if a movie is valid based on user input
def valid_movie(target_year, before_year, target_rating, film_year, film_rating):
    if float(film_rating) < float(target_rating):
        return False
    if before_year == True and int(film_year) > int(target_year):
        return False
    elif before_year == False and int(film_year) < int(target_year):
        return False
    return True

# User input and welcome screen
print(
r"""
   _                       _   _        __
  / \   ___      __       | | | |      |  |
  | |  |  _ \ _ /  |  ____| | | |____  |  |
  | |  | / \   /\  | |  --- | |  --- | |  |
  | |  | |  \_/  \ | |  |_| | |  |_| | |__|
  |_|  |_|        \| |______| |______| |__|
""")
print("Need help selecting a movie to watch? Input a few specifications for a movie,\n"
      "and a list will be generated with potential options.")

year_threshold, before = get_year_threshold()
rating_threshold = get_rating_threshold()

# Sets up BeautifulSoup object
website = rq.get('https://www.imdb.com/chart/top/')
soup = BeautifulSoup(website.content, 'html.parser')

# Obtains major elements of the movie using Beautiful Soup; sets up lists for later
film_names = soup.select("tr td a", width=45)[1:]
film_year = soup.select(".secondaryInfo")
film_ratings = soup.select("tr td strong")
list_film_names = []
list_film_years = []
list_film_ratings = []

# Puts data into lists
for i in range(len(film_year)):
    year = film_year[i].getText()
    year = year.strip("()")
    if valid_movie(year_threshold, before, rating_threshold, int(year), float(film_ratings[i].getText())) == True:
        list_film_names += [film_names[2 * i].getText()]
        list_film_years += [film_year[i].getText()]
        list_film_ratings += [film_ratings[i].getText()]

# Sets up pandas DataFrame for pretty output
if len(list_film_names) != 0:
    data = {'Film': list_film_names, 'Year': list_film_years, 'Rating': list_film_ratings}
    df = pd.DataFrame(data)
    print(df.to_string())
else:
    print("No such movies are on the top 250 IMDB films.")
