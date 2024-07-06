from bs4 import BeautifulSoup
import requests
URL = "https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(url=URL)
web_page = response.text
# print(response.text)

soup = BeautifulSoup(web_page, "html.parser")
# print(soup)

all_movies = soup.find_all(name="h3", class_="listicleItem_listicle-item__title__BfenH")
movie_titles = [movie.getText() for movie in all_movies]
movies = movie_titles[::-1]
# print(movies)

with open("movies.txt", mode="w") as file:
    for movie in movies:
        file.write(f"{movie}\n")