from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from bookstore.forms import BookForm
from bookstore.models import Book, Request_Book, Order


def Usersignup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 != password2:
                messages.info(request, "Passwords do not match.")
                return redirect('/signup')

            user = User.objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return render(request, 'user_login.html')
    return render(request, "signup.html")


def User_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            user_username = request.POST['user_username']
            user_password = request.POST['user_password']

            user = authenticate(username=user_username, password=user_password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect("/for_users")
            else:
                messages.error(request, "Please provide a valid username and password")
    return render(request, "user_login.html")


@login_required(login_url='/user_login')
def Users(request):
    books = Book.objects.all()
    total_books = books.count()

    return render(request, "for_users.html", {'books': books, 'total_books': total_books})



def Add_Books(request):
    if request.method=="POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "add_books.html")
    else:
        form=BookForm()
    return render(request, "add_books.html", {'form':form})


def see_requested_books(request):
    requested_book = Request_Book.objects.all()
    return render(request, "see_requested_books.html", {'requested_book':requested_book})


def customers_list(request):
    customers = Order.objects.all()
    customer_count = customers.count()
    return render(request, "customers_list.html", {'customers':customers, 'customer_count':customer_count})


def orders_list(request, myid):
    customer = Order.objects.filter(id=myid)
    return render(request, "orders_list.html", {'customer': customer})


def data_view(request, myid):
    orders = Order.objects.get(id=myid)
    return JsonResponse({'data': orders.items_json})


def index(request):
    return None