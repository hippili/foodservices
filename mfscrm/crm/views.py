from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect



from weasyprint import HTML


now = timezone.now()


def home(request):
    return render(request, 'crm/home.html',
                  {'crm': home})

@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/customer_list.html',
                  {'customers': customer})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/customer_list.html',
                          {'customers': customer})
    else:
        # edit
        form = CustomerForm(instance=customer)
        return render(request, 'crm/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        messages.success(request, "Customer successfully deleted!")
        return HttpResponseRedirect('/home/')
    context = {'customer': customer
               }
    return render(request, 'crm/customer_delete.html', context)

@login_required
def customer_new(request):

    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/customer_list.html',
                          {'customers': customer})
    else:
        form = CustomerForm()
        # print("Else")
    return render(request, 'crm/customer_new.html', {'form': form})

@login_required
def service_list(request):
    services = Service.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/service_list.html', {'services': services})


@login_required
def service_new(request):

    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_date = timezone.now()
            service.save()
            services = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html',
                          {'services': services})
    else:
        form = ServiceForm()
        # print("Else")
    return render(request, 'crm/service_new.html', {'form': form})


@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        #update
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            # service.customer = service.id
            service.updated_date = timezone.now()
            service.save()
            service = Service.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/service_list.html', {'services': service})
    else:
        # edit
        form = ServiceForm(instance=service)
        return render(request, 'crm/service_edit.html', {'form': form})

@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service successfully deleted!")
        return HttpResponseRedirect('/home/')
    context = {'service': service
               }
    return render(request, 'crm/service_delete.html', context)


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        #update
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            # product.customer = product.id
            product.updated_date = timezone.now()
            product.save()
            product = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html', {'products': product})

    else:
        # print("else")
        form = ProductForm(instance=product)
        return render(request, 'crm/product_edit.html', {'form': form})



@login_required
def product_list(request):
    products = Product.objects.filter(created_date__lte=timezone.now())
    return render(request, 'crm/product_list.html', {'products': products})




@login_required
def product_new(request):

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            products = Product.objects.filter(created_date__lte=timezone.now())
            return render(request, 'crm/product_list.html',
                          {'products': products})
    else:
        form = ProductForm()
        # print("Else")
    return render(request, 'crm/product_new.html', {'form': form})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product successfully deleted!")
        return HttpResponseRedirect('/home/')
    context = {'product': product
               }
    return render(request, 'crm/product_delete.html', context)


@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
    return render(request, 'crm/summary.html', {'customer': customer,
                                                'products': products,
                                                'services': services,
                                                'sum_service_charge': sum_service_charge,
                                                'sum_product_charge': sum_product_charge, })


@login_required
def product_summary(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sum_product_charge = Product.objects.filter(cust_name=product.cust_name).aggregate(Sum('charge'))
    return render(request, 'crm/product_summary.html', {
                                                'product': product,
                                                'sum_product_charge': sum_product_charge, })

@login_required
def service_summary(request, pk):
    service = get_object_or_404(Service, pk=pk)
    sum_service_charge = Service.objects.filter(cust_name=service.cust_name).aggregate(Sum('service_charge'))
    return render(request, 'crm/service_summary.html', {

                                                'service': service,
                                                'sum_service_charge': sum_service_charge, })


@login_required
def export_pdf(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
    context = {'customer': customer,
               'products': products,
               'services': services,
               'sum_service_charge': sum_service_charge,
               'sum_product_charge': sum_product_charge,
               }
    html_string = render_to_string('crm/pdf_template.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="customer-summary.pdf"'
        return response

    return response




@login_required
def product_export_pdf(request, pk):
    product = get_object_or_404(Product, pk=pk)
    sum_product_charge = Product.objects.filter(cust_name=product.cust_name).aggregate(Sum('charge'))
    context = {'product': product,
               'sum_product_charge': sum_product_charge,
               }
    html_string = render_to_string('crm/pdf_product.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="product-summary.pdf"'
        return response

    return response


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



