
from django.conf.urls import url, include
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^market/$',views.market,name='marketbase'),
    url(r'^market/(?P<childid>\d+)/(?P<sortid>\d+)/$',views.market,name='market'),

    url(r'^mine/$',views.mine,name='mine'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'checkemail/$',views.checkemail,name='checkemail'),

    url(r'^addcart/$',views.addcart,name='addcart'),
]
