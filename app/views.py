import hashlib
import random
import time

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart


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
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)


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
    if request.method == 'GET':
        return render(request,'mine/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        #重定向
        back = request.COOKIES.get('back')

        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()
            if user.password == generate_password(password):
                token = generate_token()
                cache.set(token,user.id,60*60*24*3)
                #传递给客户端
                request.session['token'] = token
                if back == 'mine':
                    return redirect('axf:mine')
                else:
                    return redirect('axf:marketbase')
            else:
                return render(request,'mine/login.html',context={'ps_err':'密码错误'})

        else:
            return render(request,'mine/login.html',context={'user_err':'用户名不存在'})





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
    print('进入1')
    if request.method == 'GET':
        return render(request,'mine/register.html')
    elif request.method == 'POST':
        print('进入2')
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
        print('进入3')
        return redirect('axf:mine')


def checkemail(request):
    email = request.GET.get('email')
    users = User.objects.filter(email=email)
    if users.exists():
        response_data = {
            'status':0,
            'msg':'帐号被占用'
        }
    else:
        response_data = {
            'status':1,
            'msg':'帐号可用'
        }

    return JsonResponse(response_data)


def addcart(request):
    token = request.session.get('token')

    response_data = {}

    if token:
        userid = cache.get(token)

        if userid:
            user = User.objects.get(pk=userid)
            goodsid = request.GET.get('goodsid')
            goods = Goods.objects.get(pk=goodsid)
            # 判断需要添加的商品是否已经存在
            carts = Cart.objects.filter(user=user).filter(goods=goods)

            if carts.exists():
                cart = carts.first()
                cart.number += 1
                cart.save()
            else:
                cart = Cart()
                cart.user = user
                cart.goods = goods
                cart.number = 1
                cart.save()
            response_data['status'] = 1
            response_data['msg'] = '添加{}购物车成功:{}'.format(cart.goods.productlongname,cart.number)

            return JsonResponse(response_data)

    response_data['status'] = -1
    response_data['msg'] = '请登录后操作'
    return JsonResponse(response_data)