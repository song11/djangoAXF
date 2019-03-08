import hashlib
import random
import time

from django.core.cache import cache
from django.shortcuts import render, redirect

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User


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





def market(request,childid='0',sortid='0'):
    # 分类数据
    foodtypes = Foodtypes.objects.all()
    # goodslist = Goods.objects.all()
    index = int(request.COOKIES.get('index','0'))
    print('index',index)
    #通过返回点击的下标识别获取分类id
    categoryid = foodtypes[index].typeid
    #子类
    if childid == '0':
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childid=childid)

    #排序
    if sortid == '1':
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '2':
        goods_list = goods_list.order_by('price')
    elif sortid == '3':
        goods_list = goods_list.order_by('-price')

    #获取子类信息
    childtypenames = foodtypes[index].childtypenames
    #字符串处理,将子类名存储到列表
    childtype_list = []
    for item in childtypenames.split('#'):
        item_arr = item.split(':')
        temp_dir = {
            'name':item_arr[0],
            'id':item_arr[1]
        }
        childtype_list.append(temp_dir)

    response_dir = {
        'foodtypes': foodtypes,
        'goods_list':goods_list,
        'childtype_list':childtype_list,
        'childid':childid,
    }


    return render(request,'market/market.html',context=response_dir)



def cart(request):
    return render(request,'cart/cart.html')


def mine(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = None
    if userid:
        user = User.objects.get(pk=userid)
    return render(request,'mine/mine.html',context={'user':user})


def login(request):
    return render(request,'mine/login.html')


def logout(request):
    request.session.flush()
    return redirect('axf:mine')


def generate_password(param):
    md5 = hashlib.md5()
    md5.update(param.encode('utf-8'))
    return md5.hexdigest()


def generate_token():
    token = str(time.time())+str(random.random())
    md5 = hashlib.md5()
    md5.update(token.encode('utf-8'))
    return md5.hexdigest()


def register(request):
    if request.method == 'GET':
        return render(request,'mine/register.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = generate_password(request.POST.get('password'))
    #需要查看数据存储是否正确
        user = User()
        user.email = email
        user.password = password
        user.name = name
        user.save()

        #状态保持
        token = generate_token()
        cache.set(token,user.id,60*60*24*3)
        request.session['token'] = token

    return redirect('axf:mine')