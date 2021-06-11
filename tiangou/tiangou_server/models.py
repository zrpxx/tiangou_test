from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'category'


class Order(models.Model):
    ordercode = models.CharField(db_column='orderCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(max_length=255, blank=True, null=True)
    post = models.CharField(max_length=255, blank=True, null=True)
    receiver = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    usermessage = models.CharField(db_column='userMessage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.
    paydate = models.DateTimeField(db_column='payDate', blank=True, null=True)  # Field name made lowercase.
    deliverydate = models.DateTimeField(db_column='deliveryDate', blank=True, null=True)  # Field name made lowercase.
    confirmdate = models.DateTimeField(db_column='confirmDate', blank=True, null=True)  # Field name made lowercase.
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'order'


class Orderitem(models.Model):
    pid = models.ForeignKey('Product', models.DO_NOTHING, db_column='pid', blank=True, null=True)
    oid = models.ForeignKey(Order, models.DO_NOTHING, db_column='oid', blank=True, null=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'orderitem'


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(db_column='subTitle', max_length=255, blank=True, null=True)  # Field name made lowercase.
    originalprice = models.FloatField(db_column='originalPrice', blank=True, null=True)  # Field name made lowercase.
    promoteprice = models.FloatField(db_column='promotePrice', blank=True, null=True)  # Field name made lowercase.
    stock = models.IntegerField(blank=True, null=True)
    cid = models.ForeignKey(Category, models.DO_NOTHING, db_column='cid', blank=True, null=True)
    createdate = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'product'


class Productimage(models.Model):
    pid = models.ForeignKey(Product, models.DO_NOTHING, db_column='pid', blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    pic = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'productimage'


class Property(models.Model):
    cid = models.ForeignKey(Category, models.DO_NOTHING, db_column='cid', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'property'


class Propertyvalue(models.Model):
    pid = models.ForeignKey(Product, models.DO_NOTHING, db_column='pid', blank=True, null=True)
    ptid = models.ForeignKey(Property, models.DO_NOTHING, db_column='ptid', blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'propertyvalue'


class User(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    isAdmin = models.BooleanField(null=False, default=False)

    class Meta:
        managed = True
        db_table = 'user'
