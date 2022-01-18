from django.shortcuts import render,HttpResponse
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()





def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'service.html')

def menu(request):
    price = cg.get_coins_markets(vs_currency='inr')
    dic = price[1]
    print(dic['id'])
    name = []
    img = []
    cr_price = []
    hi_price = []
    lo_price = []

    for i in range(len(price)):
        dicc = price[i]
        name.append(dicc['id'])
        img.append(dicc['image'])
        cr_price.append(dicc['current_price'])
        hi_price.append(dicc['high_24h'])
        lo_price.append(dicc['low_24h'])

    print(name)
    print(img)
    print(cr_price)

    mylist = zip(name, img, cr_price, hi_price, lo_price)

    return render(request, 'menu.html', {'mylist': mylist})


def booking(request):
    return render(request,'booking.html')

def testimonial(request):
    return render(request,'testimonial.html')

def team(request):
    return render(request,'team.html')

def contact(request):
    return render(request,'contact.html')