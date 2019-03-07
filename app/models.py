from django.db import models


# 基础 类
class Base(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=20)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# 轮播图 模型类
class Wheel(Base):
    class Meta:
        db_table = 'axf_wheel'


# 导航 模型类
class Nav(Base):
    class Meta:
        db_table = 'axf_nav'

# 每日必购 模型类
class Mustbuy(Base):
    class Meta:
        db_table = 'axf_mustbuy'

# 商品部分内容
class Shop(Base):
    class Meta:
        db_table = 'axf_shop'

# 商品主体
class MainShow(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=200)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=50)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=200)
    price1 = models.FloatField()
    marketprice1 = models.FloatField()

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=200)
    price2 = models.FloatField()
    marketprice2 = models.FloatField()

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=200)
    price3 = models.FloatField()
    marketprice3 = models.FloatField()

    class Meta:
        db_table = 'axf_mainshow'

    def __str__(self):
        return self.name


#商品分类
class Foodtypes(models.Model):
    # 分类id
    typeid = models.CharField(max_length=10)
    # 分类名称
    typename = models.CharField(max_length=100)
    # 子类名称
    childtypenames = models.CharField(max_length=200)
    # 分类排序(显示的先后顺序)
    typesort = models.IntegerField()

    class Meta:
        db_table = 'axf_foodtypes'

    def __str__(self):
        return self.typename

