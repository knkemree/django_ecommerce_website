from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render

from cart.forms import CartAddProductForm
from home.forms import SignUpForm
from shop.models import Category, Product
from home.models import Contact, ContactForm, CommentForm, Comment


# Create your views here.
def index(request):
    sliderlist = Product.objects.filter(available=True)[:5]
    products_lists = Product.objects.filter(available=True)
    # total item in the cart
    cart_product_form = CartAddProductForm()
    context = {
               'sliderlist': sliderlist,
               'products_lists': products_lists,
                'cart_product_form':cart_product_form,
               }
    return render(request, 'index.html', context)

def login_form(request):   #buranin ismini login koyma
    if request.method == 'POST':
        next_url = request.POST['next'] # get previous url
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if next_url:
                return redirect(next_url) #next url varsa next url'ye yonlendirir
            else:
                HttpResponse("Dara Food")
            #redirect to a success page
                return redirect('/') #next url yoksa anasayfaya yonlendirir
            # HTTP response(user.username)
        else:
            context = {'error': 'The e-mail address or password you entered was incorrect.',
                       }
            # return an 'invalid login' error message
            return render(request, "login.html", context)
    else:
        return render(request, "login.html")

def login_out(request) :
    logout(request)
    return redirect('/')

def contact_form(request) :

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contactdata = Contact()
            contactdata.name = form.cleaned_data['name']
            contactdata.email = form.cleaned_data['email']
            contactdata.subject = form.cleaned_data['subject']
            contactdata.message = form.cleaned_data['message']
            contactdata.save()

            messages.success(request, "Your message has been sent. Thank you for your interest.")
            return HttpResponseRedirect('/contact')

    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact(request):

    return render(request, 'contact.html')


@login_required(login_url='/login')
def comment_add(request, proid):
    # if this is a POST request we need to process the form data
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        # create a form  instance and populate it with data from the request
        form = CommentForm(request.POST)
        # check whether it's valid

        if form.is_valid():
            current_user = request.user
            data = Comment()
            data.product_id = proid
            data.user_id = current_user.id
            data.subject = form.cleaned_data['subject']
            data.rating = form.cleaned_data['rating']
            data.message = form.cleaned_data['message']
            data.save()

            messages.success(request, "Your review has been sent. Thank you for your interest")
            return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url)

@login_required(login_url='/login')
def comment_list(request):
    current_user =request.user
    comments = Comment.objects.filter(user=current_user.id).order_by('-id')
    context = {
        'page': 'comments',
        'comments': comments,
    }
    return render(request, "comment_list.html", context)

@login_required(login_url='/login')
def comment_delete(request, id):
    url = request.META.get('HTTP_REFERER') #bir onceki adresi alir
    Comment.objects.filter(id=id).delete()
    messages.success(request, "Comment successfully deleted")
    return HttpResponseRedirect(url)



User = get_user_model()
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            form.save()# save user form data to user table
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            #new_user = User.objects.create_user(username, email, raw_password, )
            new_user = authenticate(request, username=username, email=email, password=password,) #login after registration
            if new_user is not None:
                login(request, new_user)


            return redirect('/')
        else:
            form = SignUpForm()
            messages.success(request, "Username and email must be unique. Make sure passwords match!")
        return render(request, 'user_signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'user_signup.html', {'form': form})






