import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from django.shortcuts import render
from . import models

BASE_CRAIGSLIST_URL = 'https://bangladesh.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def search(request):
    new_search = request.POST.get('search')
    models.Search.objects.create(search=new_search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(new_search))
    response = requests.get(final_url)
    soup = BeautifulSoup(response.text, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    data = {
        'search': new_search,
        'final_postings': final_postings
    }

    return render(request, 'search_app/search.html', data)
