import datetime
import uuid

import django.db.utils
from django.core.serializers.json import DjangoJSONEncoder
from django_redis import get_redis_connection
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import QuerySet
from django.shortcuts import render
from django.views import generic

# Create your views here.
import json
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import random

r = get_redis_connection()


def checkRequestToken(request):
    token = request.META.get("HTTP_TOKEN")
    if token is None or token == '':
        return False
    try:
        value = r.get(token)
        if value is None:
            return False
        else:
            return str(value)
    except Exception:
        return False


@csrf_exempt
def login(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        user = User.objects.get(name=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Username"
        return HttpResponse(json.dumps(dic))
    if user.password != password:
        dic['message'] = "Wrong Password"
        dic['status'] = "Failed"
        return HttpResponse(json.dumps(dic))
    else:
        dic['status'] = "Success"
        dic['user_id'] = user.id
        dic['user_isAdmin'] = user.isAdmin
        dic['order_count'] = len(Order.objects.filter(uid=user))
        dic['shopping_cart_count'] = len(Orderitem.objects.filter(uid=user, oid=None))
        token = str(uuid.uuid4())
        r.set(token, 'admin' if user.isAdmin else 'user', 86400)
        dic['token'] = token
        return HttpResponse(json.dumps(dic))


@csrf_exempt
def register(request):
    dic = {}

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        user = User.objects.get(name=username)
    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Success"
        newUser = User(name=username, password=password, isAdmin=False)
        newUser.save()
        return HttpResponse(json.dumps(dic))
    if user is not None:
        dic['status'] = "Failed"
        dic['message'] = "User exist"
        return HttpResponse(json.dumps(dic))


def getUserInfo(request, user_id):
    dic = {}

    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        user = User.objects.get(id=user_id)
        dic['status'] = "Success"
        dic['order_count'] = len(Order.objects.filter(uid=user))
        dic['shopping_cart_count'] = len(Orderitem.objects.filter(uid=user, oid=None))
        return HttpResponse(json.dumps(dic))

    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "User does not exist"
        return HttpResponse(json.dumps(dic))


def getAllCategory(request):
    dic = {}

    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        category = Category.objects.all()
        cat = []
        for x in category:
            cat.append({
                'cid': x.id,
                'name': x.name
            })
        dic['categories'] = cat
        return HttpResponse(json.dumps(dic))

    except (Category.DoesNotExist):
        dic['status'] = "Failed"

    return HttpResponse(json.dumps(dic))


def createCategory(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        name = post_content['name']

        try:
            category = Category.objects.get(name=name)
        except Category.DoesNotExist:
            newCategory = Category(name=name)
            newCategory.save()
            dic['status'] = "Success"
            dic['message'] = "Category created"
            return HttpResponse(json.dumps(dic))

        dic['status'] = "Failed"
        dic['message'] = "Category already exist"
        return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def updateCategory(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        _id = post_content['id']
        newName = post_content['newName']
        try:
            category = Category.objects.get(id=_id)
            category.name = newName
            category.save()

            dic['status'] = "Success"
            dic['message'] = "Category updated"
            return HttpResponse(json.dumps(dic))
        except Category.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Category does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def deleteCategory(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'DELETE':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        _id = post_content['id']
        try:
            category = Category.objects.get(id=_id)
            category.delete()
            dic['status'] = "Success"
            dic['message'] = "Category deleted"
            return HttpResponse(json.dumps(dic))
        except Category.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Category does not exist"
            return HttpResponse(json.dumps(dic))
        except django.db.utils.IntegrityError:
            dic['status'] = "Failed"
            dic['message'] = "Category has properties, please delete properties first."
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def getAllProperty(request, category_id):
    dic = {}

    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        try:
            category = Category.objects.get(id=category_id)
            prop = Property.objects.filter(cid=category_id)
            properties = []
            for p in prop:
                properties.append(
                    {
                        'pid': p.id,
                        'name': p.name
                    }
                )
            dic['status'] = "Success"
            dic['properties'] = properties
            return HttpResponse(json.dumps(dic))

        except Category.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Category does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def createProperty(request):

    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        cid = post_content['category_id']
        name = post_content['property_name']

        try:
            category = Category.objects.get(id=cid)
            try:
                prop = Property.objects.get(name=name, cid=cid)
            except Property.DoesNotExist:
                newProp = Property(name=name, cid=category)
                newProp.save()
                dic['status'] = "Success"
                dic['message'] = "Property created"
                return HttpResponse(json.dumps(dic))

            dic['status'] = "Failed"
            dic['message'] = "Property already exist"
            return HttpResponse(json.dumps(dic))

        except Category.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Category does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def updateProperty(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        pid = post_content['property_id']
        newName = post_content['newName']
        try:
            prop = Property.objects.get(id=pid)
            prop.name = newName
            prop.save()

            dic['status'] = "Success"
            dic['message'] = "Property updated"
            return HttpResponse(json.dumps(dic))
        except Property.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Property does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def deleteProperty(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'DELETE':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        pid = post_content['property_id']
        try:
            prop = Property.objects.get(id=pid)
            prop.delete()
            dic['status'] = "Success"
            dic['message'] = "Property deleted"
            return HttpResponse(json.dumps(dic))
        except Property.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Property does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def getAllProduct(request):
    dic = {}

    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        product = Product.objects.all()
        products = []
        for p in product:
            try:
                thumbnail = Productimage.objects.get(type="thumbnail", pid=p.id).pic

            except (Productimage.DoesNotExist, AttributeError):
                thumbnail = "N/A"

            finally:
                products.append(
                    {
                        'id': p.id,
                        'name': p.name,
                        'subtitle': p.subtitle,
                        'original_price': p.originalprice,
                        'promote_price': p.promoteprice,
                        'stock': p.stock,
                        'create_date': p.createdate.strftime("%Y-%m-%d %H:%M:%S"),
                        'category_id': p.cid.id,
                        'thumbnail_pic': thumbnail
                    }
                )
        dic['status'] = "Success"
        dic['products'] = products
        return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def getProduct(request, product_id):
    dic = {}
    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        try:
            product = Product.objects.get(id=product_id)
            dic['status'] = "Success"
            dic['product'] = model_to_dict(product)
            dic['category_name'] = product.cid.name

            try:
                thumbnail = Productimage.objects.get(pid=product, type="thumbnail")
                dic['thumbnail_pic'] = thumbnail.pic
            except (Productimage.DoesNotExist, AttributeError):
                dic['thumbnail_pic'] = "N/A"

            try:
                detail = Productimage.objects.get(pid=product, type="detail")
                dic['detail_pic'] = detail.pic
            except (Productimage.DoesNotExist, AttributeError):
                dic['detail_pic'] = "N/A"

            return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder))

        except Product.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Product does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def getPropertiesOfProduct(request, product_id):
    dic = {}

    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        try:
            product = Product.objects.get(id=product_id)
            dic['status'] = "Success"
            properties = Property.objects.filter(cid=product.cid)
            property_values = []
            for p in properties:
                try:
                    value = Propertyvalue.objects.get(pid=product, ptid=p)
                    property_values.append({
                        'property': p.name,
                        'value': value.value if value.value is not None else 'N/A'
                    })
                except Propertyvalue.DoesNotExist:
                    property_values.append({
                        'property': p.name,
                        'value': 'N/A'
                    })

            dic['property'] = property_values

        except Product.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Product does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def createProduct(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        name = post_content['product_name']
        subtitle = post_content['product_subtitle']
        original_price = post_content['original_price']
        promote_price = post_content['promote_price']
        stock = post_content['product_stock']
        create_date = datetime.datetime.now()
        category_id = post_content['category_id']
        thumbnail_pic = post_content['thumbnail_pic']
        try:
            category = Category.objects.get(id=category_id)
            newProduct = Product(name=name,
                                 cid=category,
                                 subtitle=subtitle,
                                 originalprice=original_price,
                                 promoteprice=promote_price,
                                 stock=stock,
                                 createdate=create_date)
            newProduct.save()
            thumbnailPic = Productimage(pid=newProduct,
                                        type="thumbnail",
                                        pic=thumbnail_pic)
            detailPic = Productimage(pid=newProduct,
                                     type="detail")
            thumbnailPic.save()
            detailPic.save()
            dic['status'] = "Success"
            dic['message'] = "Product created"
            return HttpResponse(json.dumps(dic))

        except Category.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Category does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def updateProduct(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        pid = post_content['product_id']
        name = post_content['product_name']
        subtitle = post_content['product_subtitle']
        original_price = post_content['original_price']
        promote_price = post_content['promote_price']
        stock = post_content['product_stock']
        create_date = datetime.datetime.now()
        try:
            product = Product.objects.get(id=pid)
            product.name = name
            product.subtitle = subtitle
            product.originalprice = original_price
            product.promoteprice = promote_price
            product.stock = stock
            product.createdate = create_date
            product.save()
            dic['status'] = "Success"
            dic['message'] = "Product updated"
            return HttpResponse(json.dumps(dic))
        except Product.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Product does not exist"
            return HttpResponse(json.dumps(dic))
        except Category.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Category does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def deleteProduct(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'DELETE':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        pid = post_content['product_id']
        try:
            product = Product.objects.get(id=pid)
            try:
                thumbnailPic = Productimage.objects.get(pid=product, type="thumbnail")
                detailPic = Productimage.objects.get(pid=product, type="detail")
                thumbnailPic.delete()
                detailPic.delete()
            finally:
                product.delete()
                dic['status'] = "Success"
                dic['message'] = "Product deleted"
                return HttpResponse(json.dumps(dic))
        except Product.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Product does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def updateProductImage(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        pid = post_content['product_id']
        product = Product.objects.get(id=pid)
        thumbnailPic = Productimage.objects.get(pid=product, type="thumbnail")
        detailPic = Productimage.objects.get(pid=product, type="detail")
        try:
            newThumbnail = post_content['thumbnail']
            thumbnailPic.pic = newThumbnail
            thumbnailPic.save()
        except KeyError:
            print('No thumbnail!')
        try:
            newDetail = post_content['detail']
            detailPic.pic = newDetail
            detailPic.save()
        except KeyError:
            print('No detail!')

        dic['status'] = "Success"
        dic['message'] = "No error occurred"
        return HttpResponse(json.dumps(dic))

    except Product.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Product does not exist"
        return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def setProductPropertyValue(request):
    dic = {}

    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':

        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        pid = post_content['product_id']
        ptid = post_content['property_id']
        value = post_content['value']
        product = Product.objects.get(id=pid)
        property = Property.objects.get(id=ptid)

        try:
            verify_Property = Property.objects.get(id=ptid, cid=product.cid)
        except Property.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Product does not have this property"
            return HttpResponse(json.dumps(dic))

        try:
            product_property = Propertyvalue.objects.get(pid=product, ptid=property)
            product_property.value = value
            product_property.save()
        except Propertyvalue.DoesNotExist:
            product_property = Propertyvalue(pid=product,
                                             ptid=property,
                                             value=value)
            product_property.save()
        dic['status'] = "Success"
        dic['message'] = "Property value set successfully"
        return HttpResponse(json.dumps(dic))

    except Product.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Product does not exist"
        return HttpResponse(json.dumps(dic))

    except Property.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Property does not exist"
        return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


@transaction.atomic
def createOrder(request):
    dic = {}

    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        uid = post_content['userid']
        pids = post_content['items']
        nums = post_content['nums']
        orderInfo = post_content['orderInfo']
        try:
            user = User.objects.get(id=uid)
            for i in range(len(pids)):
                pid = pids[i]
                product = Product.objects.select_for_update().get(id=pid)
                orderItem = Orderitem.objects.get(uid=user, pid=product, oid=None)
                if orderItem.oid is not None:
                    dic['status'] = "Failed"
                    dic['message'] = "Order already exist"
                    return HttpResponse(json.dumps(dic))
                if int(product.stock) < int(nums[i]):
                    dic['status'] = "Failed"
                    dic['message'] = "Product " + product.name + " has insufficient stock"
                    return HttpResponse(json.dumps(dic))

            newOrder = Order(
                uid=user,
                ordercode=uuid.uuid4(),
                receiver=orderInfo['name'],
                mobile=orderInfo['mobile'],
                address=orderInfo['address'],
                post=orderInfo['post'],
                usermessage=orderInfo['message'],
                createdate=datetime.datetime.now(),
                status='Created'
            )
            newOrder.save()
            for i in range(len(pids)):
                pid = pids[i]
                product = Product.objects.select_for_update().get(id=pid)
                orderItem = Orderitem.objects.get(uid=user, pid=product, oid=None)
                orderItem.oid = newOrder
                orderItem.save()
                product.stock = product.stock - int(nums[i])
                product.save()

            dic['status'] = "Success"
            dic['order_id'] = newOrder.id
            return HttpResponse(json.dumps(dic))

        except User.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "User does not exist"
            return HttpResponse(json.dumps(dic))

        except Product.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Product does not exist"
            return HttpResponse(json.dumps(dic))

        except Orderitem.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Orderitem does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def getAllOrder(request):
    dic = {}

    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))

    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        order = Order.objects.all()
        orders = []
        for o in order:
            orders.append(
                {
                    'id': o.id,
                    'code': o.ordercode,
                    'address': o.address,
                    'post': o.post,
                    'receiver': o.receiver,
                    'mobile': o.mobile,
                    'userMessage': o.usermessage,
                    'createDate': o.createdate,
                    'payDate': o.paydate,
                    'shipDate': o.deliverydate,
                    'confirmDate': o.confirmdate,
                    'status': o.status
                }
            )
        dic['status'] = "Success"
        dic['orders'] = orders
        return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def getOrder(request, order_id):
    dic = {}
    
    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))
    
    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        try:
            order = Order.objects.get(id=order_id)
            dic['status'] = "Success"
            dic['order'] = model_to_dict(order)
            order_items = Orderitem.objects.filter(oid=order)
            orderItems = []
            for order_item in order_items:
                orderItems.append({
                    'name': order_item.pid.name,
                    'num': order_item.number
                })
            dic['item'] = orderItems
            return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder))

        except Order.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Order does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def getUserOrder(request, user_id):
    dic = {}
    
    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))
    
    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        user = User.objects.get(id=user_id)
        try:
            order = Order.objects.filter(uid=user)
            orders = []
            for o in order:
                orders.append(
                    {
                        'id': o.id,
                        'code': o.ordercode,
                        'address': o.address,
                        'post': o.post,
                        'receiver': o.receiver,
                        'mobile': o.mobile,
                        'userMessage': o.usermessage,
                        'createDate': o.createdate,
                        'payDate': o.paydate,
                        'shipDate': o.deliverydate,
                        'confirmDate': o.confirmdate,
                        'status': o.status
                    }
                )
            dic['status'] = "Success"
            dic['orders'] = orders
            return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder))

        except Order.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Order does not exist"
            return HttpResponse(json.dumps(dic))

    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "User does not exist"
        return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def payOrder(request):
    dic = {}
    
    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))
    
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        post_content = json.loads(request.body)
        order_id = post_content['order_id']
        order = Order.objects.get(id=order_id)
        if order.status != 'Created':
            dic['status'] = "Failed"
            dic['message'] = "Invalid order status"
            return HttpResponse(json.dumps(dic))
        else:
            order.paydate = datetime.datetime.now()
            order.status = 'Payed'
            order.save()
            dic['status'] = "Success"
            dic['message'] = "Order payed"
            return HttpResponse(json.dumps(dic))

    except Order.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Order does not exist"
        return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def deliverOrder(request):
    dic = {}
    
    if not checkRequestToken(request) or checkRequestToken(request) != 'admin':
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))
    
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        post_content = json.loads(request.body)
        order_id = post_content['order_id']
        order = Order.objects.get(id=order_id)
        if order.status != 'Payed':
            dic['status'] = "Failed"
            dic['message'] = "Invalid order status"
            return HttpResponse(json.dumps(dic))
        else:
            order.deliverydate = datetime.datetime.now()
            order.status = 'Shipped'
            order.save()
            dic['status'] = "Success"
            dic['message'] = "Order delivered"
            return HttpResponse(json.dumps(dic))

    except Order.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Order does not exist"
        return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def confirmOrder(request):
    dic = {}
    
    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))
    
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        post_content = json.loads(request.body)
        order_id = post_content['confirm_id']
        order = Order.objects.get(id=order_id)
        if order.status != 'Shipped':
            dic['status'] = "Failed"
            dic['message'] = "Invalid order status"
            return HttpResponse(json.dumps(dic))
        else:
            order.confirmdate = datetime.datetime.now()
            order.status = 'Finished'
            order.save()
            dic['status'] = "Success"
            dic['message'] = "Order confirmed."
            return HttpResponse(json.dumps(dic))

    except Order.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Order does not exist"
        return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def randomProduct(request):
    dic = {}
    
    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))
    
    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        pid = random.randint(0, Product.objects.count() - 1)
        product = Product.objects.all()[pid]
        thumbnail = Productimage.objects.get(pid=product, type="thumbnail")
        dic['status'] = "Success"
        dic['product'] = model_to_dict(product)
        dic['product_thumbnail'] = thumbnail.pic
        return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder))

    except Product.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Product / Thumbnail does not exist"
        return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def createCartProduct(request):
    dic = {}
    
    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))
    
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        product_id = post_content['pid']
        user_id = post_content['uid']
        try:
            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            try:
                orderItem = Orderitem.objects.get(uid=user, pid=product, oid=None)
                orderItem.number = orderItem.number + 1
                orderItem.save()
                dic['status'] = "Success"
                dic['message'] = "Orderitem created"
                return HttpResponse(json.dumps(dic))

            except Orderitem.DoesNotExist:
                newOrderItem = Orderitem(number=1,
                                         uid=user,
                                         pid=product)
                newOrderItem.save()
                dic['status'] = "Success"
                dic['message'] = "Orderitem created"
                return HttpResponse(json.dumps(dic))

        except Product.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Product does not exist"
            return HttpResponse(json.dumps(dic))

        except User.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "User does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def deleteCartProduct(request):
    dic = {}
    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))
    if request.method != 'DELETE':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        product_id = post_content['pid']
        user_id = post_content['uid']
        try:
            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            try:
                orderItem = Orderitem.objects.get(uid=user, pid=product, oid=None)
                orderItem.delete()
                dic['status'] = "Success"
                dic['message'] = "Orderitem deleted"
                return HttpResponse(json.dumps(dic))
            except Orderitem.DoesNotExist:
                dic['status'] = "Failed"
                dic['message'] = "Orderitem does not exist"
                return HttpResponse(json.dumps(dic))

        except Product.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Product does not exist"
            return HttpResponse(json.dumps(dic))

        except User.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "User does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def getAllCartProduct(request):
    dic = {}
    if not checkRequestToken(request):
        dic['status'] = "Failed"
        dic['message'] = "Unauthorized"
        return HttpResponse(json.dumps(dic))
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        user_id = post_content['uid']
        try:
            user = User.objects.get(id=user_id)
            orderItems = Orderitem.objects.filter(uid=user, oid=None)
            cartProducts = []
            for o in orderItems:
                cartProducts.append({
                    'pid': o.pid.id,
                    'product_name': o.pid.name,
                    'product_price': o.pid.promoteprice,
                    'number': o.number
                })
            dic['status'] = "Success"
            dic['cart_products'] = cartProducts
            return HttpResponse(json.dumps(dic))

        except User.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "User does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))
