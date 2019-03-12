import hashlib
import random
import time

from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart, Order, OrderGoods


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
    #获取购物车信息
    token = request.session.get('token')
    userid = cache.get(token)
    if userid:
        user = User.objects.get(pk=userid)
        carts = user.cart_set.all()
        response_dir['carts'] = carts

    return render(request,'market/market.html',context=response_dir)



def cart(request):
    token = request.session.get('token')
    userid = cache.get(token)
    if userid:
        user = User.objects.get(pk=userid)
        carts = user.cart_set.filter(number__gt=0)

        isall = True
        for cart in carts:
            if not cart.isselect:
                isall = False
        return render(request,'cart/cart.html',context={'carts':carts,'isall':isall})
    else:
        return render(request,'cart/no-login.html')




    return render(request,'cart/cart.html')


def mine(request):
    token = request.session.get('token')
    userid = cache.get(token)
    response_data = {
        'user' : None
    }

    if userid:
        user = User.objects.get(pk=userid)
        response_data['user'] = user
        orders = user.order_set.all()
        response_data['waitpay'] = orders.filter(status=0).count()
        response_data['paydone'] = orders.filter(status=1).count()

    return render(request,'mine/mine.html',context=response_data)


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
            response_data['number'] = cart.number
            response_data['msg'] = '添加{}购物车成功:{}'.format(cart.goods.productlongname,cart.number)

            return JsonResponse(response_data)

    response_data['status'] = -1
    response_data['msg'] = '请登录后操作'
    return JsonResponse(response_data)


def subcart(request):
    goodsid = request.GET.get('goodsid')
    goods = Goods.objects.get(pk=goodsid)

    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number -= 1
    cart.save()

    response_data = {
        'msg':'删减商品成功',
        'status':1,
        'number':cart.number,
    }
    return JsonResponse(response_data)

def changecartselect(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()
    response_data = {
        'msg':'状态修改成功',
        'status':1,
        'isselect':cart.isselect
    }

    return JsonResponse(response_data)


def changecartall(request):
    isall = request.GET.get('isall')
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)
    carts = user.cart_set.all()

    if isall == 'true': #python 区分大小写
        isall = True
    else:
        isall = False
    for cart in carts:
        cart.isselect = isall
        cart.save()

    response_data = {
        'msg':'全选/取消全选 成功',
        'status':1,
    }
    return JsonResponse(response_data)

def generate_identifier():
    temp = str(time.time())+str(random.randrange(1000,10000))
    return temp

def generateorder(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    order = Order()
    order.user = user
    order.identifier = generate_identifier()
    order.save()

    carts = user.cart_set.filter(isselect=True)
    # 创建订单商品表
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.order = order
        orderGoods.goods = cart.goods
        orderGoods.number = cart.number
        orderGoods.save()
        cart.delete()

    return render(request,'order/orderdetail.html',context={'order':order})


def orderlist(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    orders = user.order_set.all()
    return render(request,'order/orderlist.html',context={'orders':orders})


def orderdetail(request,identifier):
    order = Order.objects.filter(identifier=identifier).first()
    return render(request,'order/orderdetail.html',context={'order':order})