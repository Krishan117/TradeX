from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
from pycoingecko import CoinGeckoAPI
from newsapi import NewsApiClient
from django.contrib.auth import authenticate,login,logout
cg = CoinGeckoAPI()
import requests
import json
import pandas as pd
import pytz
import calendar
import datetime
from myapp.forms import *

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
    print(type(price))
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


def booking(request,name):
    # to timestemp
    print(name)
    date = datetime.datetime.utcnow()
    utc_time = (str(calendar.timegm(date.utctimetuple())))
    # print(type(utc_time))

    # from timestamp

    future = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
    p1 = (str(calendar.timegm(future.timetuple())))
    # print(p1)
    id = name.lower()
    graph = cg.get_coin_market_chart_range_by_id(id, vs_currency='inr', from_timestamp=p1,
                                                 to_timestamp=utc_time)
    # print(graph.keys())
    g1 = graph['prices']
    g2 = []
    g3 = []
    time1 = []
    mainlist = []
    for prices in g1:
        g2.append(prices[0])
        g3.append(prices[1])

    for i in g2:
        t1 = pd.to_datetime(i, utc=True, unit='ms')
        st = str(t1.time())
        time1.append(st)
    # print(time1)
    s = []
    for i in range(len(time1)):
        x = time1[i]
        sp = x.split(":")
        ns = []
        for j in sp:
            a = float(j)
            ns.append(int(round(a)))
        s.append(ns)
    # print(s)

    for i in range(len(g3)):
        lis = [s[i], g3[i]]
        mainlist.append(lis)

    # print(mainlist)
    # print(g1)
    # cl= zip(g2, g3)
    return render(request, 'booking.html', {'g1': g1, 'g2': g2, 'mainlist': mainlist, 's': s, 'id': id})
def testimonial(request):

    return render(request, 'testimonial.html')

def team(request):
    return render(request,'team.html')

def contact(request):
    return render(request,'contact.html')

def register(request):
    if request.method == "POST":
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            form = UserForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.set_password(request.POST.get('password'))
                obj.save()
                return redirect('index')
            else:
                print(form.errors)
                return HttpResponse('invalid')
        else:
            return HttpResponse('Password Does Not Match')
    return render(request,'index.html')

def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return HttpResponse('Invalid')
        else:
            return HttpResponse('auth Failed')
def log_out(request):
    logout(request)
    return redirect('index')


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = []
        chartLabel = "my data"
        chartdata = [0, 10, 5, 2, 20, 30, 45]
        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
        }
        return Response(data)