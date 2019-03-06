
from django.conf.urls import url, include
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^cart/$',views.cart,name='cart'),
    url(r'^market/$',views.market,name='market'),
    url(r'^mine/$',views.mine,name='mine'),
]
