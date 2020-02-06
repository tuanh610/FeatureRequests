from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import ClientDetail, Request
from .forms import RequestForm
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('new_request/', views.new_request, name='new_request'),
#     path('admin_login/', views.admin_login, name='admin_login'),
#     path('all_requests/', views.all_requests, name='all_requests'),
# ]


def home(request):
    return render(request, 'home.html')


def edit_request(request):
    if request.method == "POST":
        try:
            request_id = request.POST["id"]
            item = Request.objects.get(pk=request_id)
            request_form = RequestForm(instance=item)
            return render(request, template_name='RequestManager/edit_request.html',
                          context={"form": request_form, "request_id": request_id})
        except ObjectDoesNotExist:
            return render(request, template_name='home.html',
                          context={"error_message": "Request ID incorrect. Cannot find request"})
    else:
        return render(request, template_name='home.html',
                      context={"error_message": "Invalid request"})


def delete_request(request):
    if request.method == "POST":
        try:
            request_id = request.POST["id"]
            item = Request.objects.get(pk=request_id)
            client = ClientDetail.objects.get(pk=item.client.id)
            client.request_amount -= 1
            client.save()
            item.delete()

            return render(request, template_name='home.html', context={"status_message": "Delete request successfully"})
        except ObjectDoesNotExist:
            return render(request, template_name='home.html',
                          context={"error_message": "Request ID incorrect. Cannot find request"})
    else:
        return render(request, template_name='home.html',
                      context={"error_message": "Invalid request"})

def new_request(request):
    request_form = RequestForm()
    return render(request, template_name='RequestManager/new_request.html', context={"form": request_form})


def request_result(request):
    try:
        if request.method == "POST":
            if "cancel" in request.POST:
                return redirect('RequestManager:home')
            if "request_id" in request.POST:
                olditem = Request.objects.get(pk=request.POST["request_id"])
                requestform = RequestForm(request.POST, instance=olditem)
            else:
                requestform = RequestForm(request.POST)

            if requestform.is_valid():
                item = updateDB(requestform)
            else:
                return render(request, 'RequestManager/request_result.html',
                              {'error': "Data Input Incorrect. Please re-check"})

            return render(request, 'RequestManager/request_result.html', {'time': item.submit_date})
        else:
            return redirect('RequestManager:new_request')
    except Exception as e:
        return render(request, 'RequestManager/request_result.html', {'error': str(e)})

def updateDB(requestform):
    item = requestform.save()
    client_detail = ClientDetail.objects.get(pk=item.client.id)
    client_detail.request_amount += 1
    client_detail.save()
    current_priority = item.client_priority
    current_id = item.id

    while True:
        update_required = Request.objects.filter(client__client_name=item.client.client_name).filter(
            client_priority=current_priority).exclude(id=current_id)
        if len(update_required) == 0:
            break
        elif len(update_required) == 1:
            update_required[0].client_priority += 1
            update_required[0].save()
            current_priority += 1
            current_id = update_required[0].id
        else:
            raise Exception("Request data has been tampered. Please use admin to correct it")
    return item

def all_requests(request, page):
    all_requests = list(Request.objects.all())
    paginator = Paginator(all_requests, 12)
    allData = paginator.get_page(page)
    return render(request, 'RequestManager/all_requests.html', {'allData': allData})


class RequestView(generic.DetailView):
    model = Request
    template_name = 'RequestManager/detail.html'
    context_object_name = 'request_item'

def about(request):
    return render(request, 'about.html')
