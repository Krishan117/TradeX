from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from plotly import *
import plotly.graph_objects as go
from dash import *
from pycoingecko import CoinGeckoAPI
from newsapi import NewsApiClient
from django.core.paginator import *
from django.contrib.auth import authenticate, login, logout

cg = CoinGeckoAPI()
import requests
import json
import pandas as pd
import pytz
import calendar
import datetime
from myapp.forms import *


def index(request):

    context = {}
    # Trending Crypto
    trending = cg.get_search_trending(vs_currency='inr')
    l1 = trending['coins']
    # print(l1)
    mydic = {}
    name1 = []
    img1 = []
    price1 = []
    id1 = []
    for i in l1:
        mydic = i["item"]
        for j in i.values():
            name1.append(j["name"])
            img1.append(j["large"])
            price1.append(j["price_btc"])
            id1.append(j['id'])
            cryptrendlist = zip(name1, img1, price1, id1)
            context['cryptrendlist'] = cryptrendlist

    #  # top-gainers
    #     url = "https://latest-stock-price.p.rapidapi.com/any"
    #     headers = {
    #         'x-rapidapi-host': "latest-stock-price.p.rapidapi.com",
    #         'x-rapidapi-key': "a0cbf7e4a6msh8774514d0c1c6c5p1e0d80jsn3374cad14b76"
    #     }
    #     response = requests.request("GET", url, headers=headers)
    #     l1 = response.text
    #     a = json.loads(l1)
    #     s_name = []
    #     s_price = []
    #     d_high = []
    #     d_low = []
    #     s_change = []
    #     p_change = []
    #
    #     for j in range(len(a)):
    #         s_dic = a[j]
    #         s_name.append(s_dic['symbol'])
    #         s_price.append(s_dic['lastPrice'])
    #         d_high.append(s_dic['dayHigh'])
    #         d_low.append(s_dic['dayLow'])
    #         s_change.append(s_dic['change'])
    #         p_change.append(s_dic['pChange'])
    #
    #     l2 = zip(s_name, s_price, d_high, d_low, s_change, p_change)
    #
    #     tgs_name = s_name[1:11]
    #     tgs_price = s_price[1:11]
    #     tgd_high = d_high[1:11]
    #     tgd_low = d_low[1:11]
    #     tgs_change = s_change[1:11]
    #     tgp_change = p_change[1:11]
    # # top-loosers
    #     tls_name = s_name[658:668]
    #     tls_price = s_price[658:668]
    #     tld_high = d_high[658:668]
    #     tld_low = d_low[658:668]
    #     tls_change = s_change[658:668]
    #     tlp_change = p_change[658:668]
    #     top_gainers = zip(tgs_name, tgs_price, tgd_high, tgd_low, tgs_change, tgp_change)
    #     top_loosers = zip(tls_name, tls_price, tld_high, tld_low, tls_change, tlp_change)

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
    context['list1'] = list1
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def service(request):
    context = {}
    cs_list = cg.get_coin_ohlc_by_id(id='bitcoin', vs_currency='inr', days='14')
    gt1 = cs_list

    gt2 = []
    time2 = []
    for l1 in cs_list:
        tme = l1[0] + 19800000
        gt2.append(tme)
    for i in gt2:
        r1 = pd.to_datetime(i, utc=False, unit='ms')
        st1 = str(r1)
        time2.append(st1)
        a_dataframe = pd.DataFrame(time2)
        context['a_dataframe'] = a_dataframe
        b_dataframe = pd.DataFrame(cs_list)
        context['dataframe'] = b_dataframe

        # print(a_dataframe,b_dataframe)
        fig = go.Figure(data=[go.Candlestick(x=a_dataframe[0],
                                             open=b_dataframe[1],
                                             high=b_dataframe[2],
                                             low=b_dataframe[3],
                                             close=b_dataframe[4])])
        candlestick_div = plot(fig, output_type='div')
        context['candlestick_div'] = candlestick_div
    return render(request, 'service.html', context)


def menu(request):

    context = {}
    #  FOR CRYPTO
    price = cg.get_coins_markets(vs_currency='inr')
    name = []
    img = []
    cr_price = []
    hi_price = []
    lo_price = []
    rank = []
    id1 = []
    # print(price)
    for i in range(len(price)):
        dicc = price[i]
        # print(dicc)
        name.append(dicc['name'])
        img.append(dicc['image'])
        cr_price.append(dicc['current_price'])
        hi_price.append(dicc['high_24h'])
        lo_price.append(dicc['low_24h'])
        rank.append(dicc['market_cap_rank'])
        id1.append(dicc['id'])
    mylist = zip(name, img, cr_price, hi_price, lo_price, rank, id1)
    context['page_obj'] = mylist
    # p = Paginator(mylist, 10)
    # page_number = request.GET.get('page')
    # try:
    #     page_obj = p.get_page(page_number)
    # except PageNotAnInteger:
    #     page_obj = p.page(1)
    # except EmptyPage:
    #     page_obj = p.page(p.num_pages)
    # context['page_obj'] = page_obj

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

    l2 = zip(s_name, s_price, d_high, d_low, s_change, p_change)
    context['l2'] = l2
    return render(request, 'menu.html', context)


def booking(request, id1):
    # to timestamp(24 hours)
    context = {}

    date = datetime.datetime.utcnow()
    utc_time = (str(calendar.timegm(date.utctimetuple())))

    # from timestamp(24 hours)

    future = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    p1 = (str(calendar.timegm(future.timetuple())))
    name = id1.upper()
    context['name'] = name
    id = id1
    context['id'] = id

    graph = cg.get_coin_market_chart_range_by_id(id, vs_currency='inr', from_timestamp=p1,
                                                 to_timestamp=utc_time)
    # print(graph)
    g1 = graph['prices']
    context['g1'] = g1
    g2 = []
    g3 = []
    time1 = []
    for prices in g1:
        time = prices[0] + 19800000
        g2.append(time)
        g3.append(prices[1])

    for i in g2:
        t1 = pd.to_datetime(i, utc=False, unit='ms')
        st = str(t1.time())
        time1.append(st)
        context['time1'] = time1
        # print(time1)

    # to timestamp(30 days)
    date = datetime.datetime.utcnow()
    utc_time = (str(calendar.timegm(date.utctimetuple())))

    # from timestamp(30 days)

    future = datetime.datetime.utcnow() - datetime.timedelta(weeks=4.34524)
    p2 = (str(calendar.timegm(future.timetuple())))
    # name = id1.upper()
    id = id1

    graph30 = cg.get_coin_market_chart_range_by_id(id, vs_currency='inr', from_timestamp=p2,
                                                   to_timestamp=utc_time)
    # print(graph30)
    gt1 = graph30['prices']
    context['gt1'] = gt1
    gt2 = []
    time2 = []
    for prices in gt1:
        tme = prices[0] + 19800000
        gt2.append(tme)

    for i in gt2:
        r1 = pd.to_datetime(i, utc=False, unit='ms')
        st1 = str(r1.date())
        time2.append(st1)
        context['time2'] = time2
        # print(time2)

    # to timestamp(1 year)
    date = datetime.datetime.utcnow()
    utc_time = (str(calendar.timegm(date.utctimetuple())))

    # from timestamp(1 year)

    future = datetime.datetime.utcnow() - datetime.timedelta(weeks=52.1786)
    p3 = (str(calendar.timegm(future.timetuple())))
    # name = id1.upper()
    id = id1

    graph1 = cg.get_coin_market_chart_range_by_id(id, vs_currency='inr', from_timestamp=p3,
                                                  to_timestamp=utc_time)
    # print(graph30)
    gy1 = graph1['prices']
    context['gy1'] = gy1
    gy2 = []
    time3 = []
    for prices in gy1:
        tme = prices[0] + 19800000
        gy2.append(tme)

    for i in gy2:
        r1 = pd.to_datetime(i, utc=False, unit='ms')
        st1 = str(r1.date())
        time3.append(st1)
        context['time3'] = time3
    # print(time2)
    return render(request, 'booking.html', context)


def testimonial(request):
    return render(request, 'testimonial.html')


def team(request):
    return render(request, 'team.html')


def contact(request):
    return render(request, 'contact.html')


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
    return render(request, 'index.html')


def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('Invalid')
        else:
            return HttpResponse('auth Failed')


def log_out(request):
    logout(request)
    return redirect('index')


