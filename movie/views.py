from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "movie/movie_name.html")


import requests
from bs4 import BeautifulSoup

def find_movie_url(movie_name):
    movie_name = movie_name.replace(' ', '%20')
    movie_list_url = f"https://www.imdb.com/find?q={movie_name}&s=tt&ttype=ft"

    movies_list = requests.get(movie_list_url)
    movies_soup = BeautifulSoup(movies_list.text, "lxml")
    first_movie_href = movies_soup.find('table', class_="findList").find('tr').find('td', class_="result_text").a['href']

    first_movie_url = f"https://www.imdb.com{first_movie_href}"

    return first_movie_url


def movie_information(url):
    context = {}

    try:
        source = requests.get(url)
        source.raise_for_status()
        
        soup = BeautifulSoup(source.text, "lxml")

        img = soup.find('div', class_="ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img").img
        img_src = img['src']
        context['img'] = img_src

        div_tag = soup.find('div', class_="sc-80d4314-0 fjPRnj").find('div', class_="sc-80d4314-1 fbQftq")
        title = div_tag.h1
        context['title'] = title.text

        year = soup.find('div', class_="sc-80d4314-2 iJtmbR").ul.select_one(":nth-child(1)").span
        context['year'] = year.text

        rating = soup.find('div', class_="sc-7ab21ed2-2 kYEdvH")
        context['rating'] = rating.text

        director = soup.find('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        context['director'] = director.text

        about = soup.find('span', class_="sc-16ede01-1 kgphFu")
        context['summary'] = about.get_text()

        return context


    except Exception as e:
        print(e)

def information(request):
    context = {}
    movie_name = request.POST.get("name")

    url = find_movie_url(movie_name)
    context = movie_information(url)

    return render(request, "movie/information.html", context)