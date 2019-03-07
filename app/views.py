from django.shortcuts import render

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes


def home(request):
    # 轮播图数据
    wheels = Wheel.objects.all()

    # 导航 数据
    navs = Nav.objects.all()

    # 每日必购
    mustbuys = Mustbuy.objects.all()

    # 商品部分
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]

    # 商品主体
    mainshows = MainShow.objects.all()

    data = {
        'title': '首页',
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead': shophead,
        'shoptab': shoptab,
        'shopclass': shopclass,
        'shopcommend': shopcommend,
        'mainshows':mainshows,
    }

    return render(request,'home/home.html',context=data)


def cart(request):
    return render(request,'cart/cart.html')


def market(request):
    # 分类数据
    foodtypes = Foodtypes.objects.all()

    data = {
        'foodtypes': foodtypes,
    }


    return render(request,'market/market.html',context=data)


def mine(request):
    return render(request,'mine/mine.html')