import requests
import time
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import randint

base_url = 'https://www.imdb.com/chart/top'
request_delay = 15
num_pages = 5
csv_file = 'imdb_top_movies.csv'


def scrape_imdb_top_movies():
    with open(csv_file, 'w', newline='\n', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Title', 'Rating', 'Year'])

    for page in range(1, num_pages + 1):
        url = f'{base_url}?sort=rk,asc&mode=simple&page={page}'

        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        movie_data = []

        movies = soup.find_all('td', class_='titleColumn')

        for movie in movies:
            rank = movie.get_text(strip=True).split('.')[0]
            title = movie.a.get_text(strip=True)
            rating = movie.find_next_sibling('td', class_='ratingColumn').strong.get_text(strip=True)
            year = movie.span.get_text(strip=True, separator='()')

            movie_data.append([rank, title, rating, year])

        with open(csv_file, 'a', newline='\n', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(movie_data)

        time.sleep(request_delay)

    print('მონაცემები შენახულია Csv ფაილში ✅')


scrape_imdb_top_movies()
