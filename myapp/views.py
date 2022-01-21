from django.shortcuts import render,HttpResponse
from pycoingecko import CoinGeckoAPI
from newsapi import NewsApiClient
cg = CoinGeckoAPI()
import requests
import json


def index(request):
    # Trending Crypto
    trending = cg.get_search_trending(vs_currency='inr')
    l1 = trending['coins']
    # print(l1)
    mydic = {}
    name1 = []
    img1 = []
    price1 = []
    for i in l1:
        mydic = i["item"]
        for j in i.values():
            name1.append(j["name"])
            img1.append(j["large"])
            price1.append(j["price_btc"])
            cryptrendlist = zip(name1, img1, price1)

    # top-headlines
    newsapi = NewsApiClient(api_key='6e7eacc7bb504b55a56f04a05456b9f5')
    top = newsapi.get_top_headlines(country='in', category='business')
    articles = top['articles']
    # print(articles)
    n_img = []
    title = []
    dec = []
    for i in range(len(articles)):
        dic = articles[i]
        n_img.append(dic['urlToImage'])
        title.append(dic['title'])
        dec.append(dic['description'])

    list1 = zip(n_img, title, dec)
    return render(request, 'index.html', {'list1': list1, 'cryptrendlist': cryptrendlist})

def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'service.html')

def menu(request):
    #  FOR CRYPTO
    price = cg.get_coins_markets(vs_currency='inr')
    name = []
    img = []
    cr_price = []
    hi_price = []
    lo_price = []
    rank = []

    for i in range(len(price)):
        dicc = price[i]
        name.append(dicc['name'])
        img.append(dicc['image'])
        cr_price.append(dicc['current_price'])
        hi_price.append(dicc['high_24h'])
        lo_price.append(dicc['low_24h'])
        rank.append(dicc['market_cap_rank'])
    mylist = zip(name, img, cr_price, hi_price, lo_price, rank)

    # FOR STOCKS
    url = "https://latest-stock-price.p.rapidapi.com/any"
    headers = {
        'x-rapidapi-host': "latest-stock-price.p.rapidapi.com",
        'x-rapidapi-key': "a0cbf7e4a6msh8774514d0c1c6c5p1e0d80jsn3374cad14b76"
    }
    response = requests.request("GET", url, headers=headers)
    l1 = response.text
    a = json.loads(l1)
    s_name = []
    s_price = []
    d_high = []
    d_low = []
    s_change = []
    p_change = []

    for j in range(len(a)):
        s_dic = a[j]
        s_name.append(s_dic['symbol'])
        s_price.append(s_dic['lastPrice'])
        d_high.append(s_dic['dayHigh'])
        d_low.append(s_dic['dayLow'])
        s_change.append(s_dic['change'])
        p_change.append(s_dic['pChange'])
        # if a[0:9]:
        #     break

    l2 = zip(s_name, s_price, d_high, d_low, s_change, p_change)
    return render(request, 'menu.html', {'mylist': mylist, 'l2': l2})


def booking(request):
    return render(request, 'booking.html')

def testimonial(request):
    return render(request,'testimonial.html')

def team(request):
    return render(request,'team.html')

def contact(request):
    return render(request,'contact.html')