from django import views
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from django.db.models import Q
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import  messages
from django.contrib.auth.decorators import  login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        context = {
            'topwears' : topwears,
            'bottomwears' : bottomwears,
            'mobiles' : mobiles,
            'laptops' : laptops
        }
        print('topwears:',topwears)
        print('bottomwears:-',bottomwears)
        print('mobiles:-',mobiles)
        print('laptops:-',laptops)
        print()
        return render(request, 'app/home.html',context)


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetaileView(View):
    def get(self,request,pk):
        totalitems = 0      
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        print(item_already_in_cart)
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitems':totalitems})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    print("user :- ",user)
    print("producat id :- ",product_id)
    
    Cart(user=user,product=product).save()
    print("add cart success.")
    # return render(request, 'app/addtocart.html')
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)

        amount = 0.0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discoounted_price)
                amount += tempamount
            total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'amount':amount,'totalamount':total_amount})
        else:
            return render(request,'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()

        amount = 0.0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        
        for p in cart_product:
            tempamount = (p.quantity * p.product.discoounted_price)
            amount += tempamount
        
        # total_amount = amount + shipping_amount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()

        amount = 0.0
        shipping_amount = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        
        for p in cart_product:
            tempamount = (p.quantity * p.product.discoounted_price)
            amount += tempamount
        
        # total_amount = amount + shipping_amount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        print(prod_id)
        print(c)
        c.delete()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        print(cart_product)
        
        for p in cart_product:
            tempamount = (p.quantity * p.product.discoounted_price)
            amount += tempamount
        
        # total_amount = amount + shipping_amount

        data = {
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{"order_placed":op})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    if data==None:
        mobiles = Product.objects.filter(category='M')
        print(mobiles)
    elif data == 'motorola' or data == 'Motorola' :
        mobiles = Product.objects.filter(category='M').filter(Q(brand ='motorola') | Q(brand ='Motorola'))
        print(mobiles)
    elif data == 'Vivo':
        mobiles = Product.objects.filter(category='M').filter(brand='Vivo')
        print(mobiles)
    
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discoounted_price__lt=10000)
        print(mobiles)
    
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discoounted_price__gt=10000)
        print(mobiles)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})


def laptop(request,data=None):
    if data==None:
        laptops = Product.objects.filter(category='L')
        print(laptops)
    elif data == 'Lenovo':
        laptops = Product.objects.filter(category='L').filter(Q(brand ='Lenovo') )
        print(laptops)
    elif data == 'Apple':
        laptops = Product.objects.filter(category='L').filter(brand='Apple')
        print(laptops)
    
    elif data == 'HP':
        laptops = Product.objects.filter(category='L').filter(brand='HP')
        print(laptops)
    
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discoounted_price__lt=35000)
        print(laptops)
    
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discoounted_price__gt=35000)
        print(laptops)
    return render(request, 'app/laptop.html',{'laptops':laptops})

def topwear(request,data=None):
    if data==None:
        topwears = Product.objects.filter(category='TW')
        print(topwears)
    elif data == 'Raymond' :
        topwears = Product.objects.filter(category='TW').filter(Q(brand ='Raymond') | Q(brand ='raymonds') | Q(brand ='raymonds'))
        print(topwears)
    elif data == 'cotton_candy':
        topwears = Product.objects.filter(category='TW').filter(brand='cotton candy')
        print(topwears)
    
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discoounted_price__lt=700)
        print(topwears)
    
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discoounted_price__gt=700)
        print(topwears)
    return render(request, 'app/topwear.html',{'topwears':topwears})

def bottomwear(request,data=None):
    if data==None:
        bottomwears = Product.objects.filter(category='BW')
        print(bottomwears)
    elif data == 'Raymond' :
        bottomwears = Product.objects.filter(category='BW').filter(Q(brand ='Raymond') | Q(brand ='raymonds') | Q(brand ='raymonds'))
        print(bottomwears)
    elif data == 'cotton_candy':
        bottomwears = Product.objects.filter(category='BW').filter(Q(brand='cotton candy') | Q(brand='Cotton candhy'))
        print(bottomwears)
    elif data == 'lee':
        bottomwears = Product.objects.filter(category='BW').filter(Q(brand='lee'))
        print(bottomwears)
    elif data == 'stylises':
        bottomwears = Product.objects.filter(category='BW').filter(Q(brand='stylises'))
        print(bottomwears)
    elif data == 'rebock':
        bottomwears = Product.objects.filter(category='BW').filter(Q(brand='rebock'))
        print(bottomwears)
    
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discoounted_price__lt=700)
        print(bottomwears)
    
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW').filter(discoounted_price__gt=700)
        print(bottomwears)
    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistraionView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations!! Registred Successfully.')
        return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 70
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    print(cart_product)
    
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discoounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    
    return redirect("orders")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            reg = Customer(user=usr,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
            reg.save()
            print(usr," ",name," ",locality," ",city," ",zipcode," ",state," **")
            messages.success(request,'Congratulations!! Profile Upadated Successfully.')

        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})


        # reach vedio 06:02