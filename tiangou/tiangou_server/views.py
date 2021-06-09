import datetime

from django.core.serializers.json import DjangoJSONEncoder
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


def getAllUser(request):
    dic = {}
    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        try:
            user = User.objects.all()
            users = []
            for u in user:
                users.append(
                    {
                        'id': u.id,
                        'name': u.name,
                        'isAdmin': u.isAdmin
                    }
                )
            dic['status'] = "Success"
            dic['users'] = users
            return HttpResponse(json.dumps(dic))

        except Category.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Category does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

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
            cat.append(x.name)
        dic['categories'] = cat
        return HttpResponse(json.dumps(dic))

    except (Category.DoesNotExist):
        dic['status'] = "Failed"

    return HttpResponse(json.dumps(dic))


def createCategory(request):
    dic = {}
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
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        name = post_content['name']
        newName = post_content['newName']
        try:
            category = Category.objects.get(name=name)
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
    if request.method != 'DELETE':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        name = post_content['name']
        try:
            category = Category.objects.get(name=name)
            category.delete()
            dic['status'] = "Success"
            dic['message'] = "Category deleted"
            return HttpResponse(json.dumps(dic))
        except Category.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Category does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def getAllProperty(request, category_id):
    dic = {}
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
                prop = Property.objects.get(name=name)
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
            products.append(
                {
                    'id': p.id,
                    'name': p.name,
                    'subtitle': p.subtitle,
                    'original_price': p.originalprice,
                    'promote_price': p.promoteprice,
                    'stock': p.stock,
                    'create_date': p.createdate.strftime("%Y-%m-%d %H:%M:%S"),
                    'category_id': p.cid.id
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
            return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder))

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
                                        type="thumbnail")
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
        category_id = post_content['category_id']
        try:
            category = Category.objects.get(id=category_id)
            product = Product.objects.get(id=pid)
            product.name = name
            product.subtitle = subtitle
            product.originalprice = original_price
            product.promoteprice = promote_price
            product.stock = stock
            product.createdate = create_date
            product.cid = category
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
            thumbnailPic.pic = newThumbnail.encode('utf-8')
            thumbnailPic.save()
        except KeyError:
            print('No thumbnail!')
        try:
            newDetail = post_content['detail']
            detailPic.pic = newDetail.encode('utf-8')
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


def getAllOrder(request):
    dic = {}
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
    if request.method != 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        try:
            order = Order.objects.get(id=order_id)
            dic['status'] = "Success"
            dic['order'] = model_to_dict(order)
            return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder))

        except Order.DoesNotExist:
            dic['status'] = "Failed"
            dic['message'] = "Order does not exist"
            return HttpResponse(json.dumps(dic))

    except (KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "Invalid input"

    return HttpResponse(json.dumps(dic))


def updateOrder(request):
    dic = {}
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
