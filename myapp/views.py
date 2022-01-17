from django.shortcuts import render,HttpResponse
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
global price, list1, market, vc
# price = cg.get_price(ids='bitcoin,litecoin', vs_currencies='inr,eur')
market = cg.get_coins_markets(vs_currency='inr')
# ids = cg.get_coin_by_id()
# list1 = cg.get_coins_list(ids='', name='', symbol='')
# for i in range (len(ids)):
vc = cg.get_coins_list()



def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'service.html')

def menu(request):
    for i in range(0, len(vc)):
        print(vc[i])
        local_vc = len(vc)
        print(local_vc)
    return render(request,'menu.html', {"local_vc": local_vc})

def booking(request):
    print('########################',type(vc))
    # print(market)
    # print(vc)
    local_price = market

    return render(request,'booking.html', {"local_price": local_price})

def testimonial(request):
    return render(request,'testimonial.html')

def team(request):
    return render(request,'team.html')

def contact(request):
    return render(request,'contact.html')