"""
This holds all the views used in the RequestManager application
The logic when render the view or when submit form is also handle here
"""
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import ClientDetail, Request
from .forms import RequestForm
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from datetime import date


def home(request):
    """
    Home page, just render 'home.html'
    """
    return render(request, 'home.html')


def edit_request(request):
    """
    Edit Page for Request
    Only accept POST request, basically means that user cannot use link copied
    to get to the page

    Return
    ----------
    If GET request
    -> redirect to request_result with "Invalid operation" error

    If "id" parameter is inside POST -> go from Detail Page to Edit Page
    -> Show a pre populated edit page

    If "request_id" parameter is inside POST -> Edit submit button is clicked
    -> Perform checking and redirect to the request_result view
       with either status when success or error when fail
    """
    if request.method == "POST":
        if "id" in request.POST:
            try:
                request_id = request.POST["id"]
                item = Request.objects.get(pk=request_id)
                request_form = RequestForm(instance=item)
                return render(request, template_name='RequestManager/edit_request.html',
                              context={"form": request_form, "request_id": request_id})
            except ObjectDoesNotExist:
                return redirect('RequestManager:request_result_error',
                                "Request ID incorrect. Cannot find request", permanent=True)
        elif "request_id" in request.POST:
            olditem = Request.objects.get(pk=request.POST["request_id"])
            requestform = RequestForm(request.POST, instance=olditem)
            if requestform.is_valid():
                if requestform.cleaned_data.get('target_date') < date.today():
                    return redirect('RequestManager:request_result_error',
                                    "Target Date cannot be earlier than current date", permanent=True)
                item = updateDB(requestform)
            else:
                return redirect('RequestManager:request_result_error',
                                "Data Input Incorrect. Please re-check", permanent=True)

            return redirect('RequestManager:request_result_ok', "Request edited at {}".format(str(item.submit_date)), permanent=True)
    else:
        return redirect('RequestManager:request_result_error',
                        "Invalid operation", permanent=True)


def delete_request(request):
    """
    Delete request
    Only accept POST request, basically means that user cannot use link copied
    to get to the page

    Return
    ----------
    If GET request
    -> redirect to request_result with "Invalid operation" error

    If "id" of the Request is not found
    -> Redirect to the request_result view with error Request not found

    If "id" of the Request is found-
    -> Delete the request, update the request_amount of respective client
       Then redirect to the request_result view with status Request deleted
    """
    if request.method == "POST":
        try:
            request_id = request.POST["id"]
            item = Request.objects.get(pk=request_id)
            client = ClientDetail.objects.get(pk=item.client.id)
            client.request_amount -= 1
            client.save()
            item.delete()

            return redirect('RequestManager:request_result_ok', "Request deleted", permanent=True)
        except ObjectDoesNotExist:
            return redirect('RequestManager:request_result_error',
                            "Request ID incorrect. Cannot find request", permanent=True)
    else:
        return redirect('RequestManager:request_result_error',
                        "Invalid operation", permanent=True)


def new_request(request):
    """
    Delete request
    Only accept POST request, basically means that user cannot use link copied
    to get to the page

    Return
    ----------
    If GET request
    -> redirect to request_result with "Invalid operation" error

    If "id" of the Request is not found
    -> Redirect to the request_result view with error Request not found

    If "id" of the Request is found-
    -> Delete the request, update the request_amount of respective client
       Then redirect to the request_result view with status Request deleted
    """
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('RequestManager:home')
        requestform = RequestForm(request.POST)
        if requestform.is_valid():
            if requestform.cleaned_data.get("target_date") < date.today():
                return redirect('RequestManager:request_result_error',
                                "Target Date cannot be earlier than current date", permanent=True)
            item = updateDB(requestform)
        else:
            return redirect('RequestManager:request_result_error', "Data Input Incorrect. Please re-check", permanent=True)

        return redirect('RequestManager:request_result_ok', "Request added at {}".format(str(item.submit_date)), permanent=True)
    else:
        request_form = RequestForm()
        response = render(request, template_name='RequestManager/new_request.html', context={"form": request_form})
        response['Cache-Control'] = 'no-cache'
        return response


def request_result(request, status=None, error=None):
    """
    Show result after add/edit/delete operation

    Return
    ----------
    If status exist:
    -> render request_result.html with status parameter

    If error exist:
    -> render request_result.html with error parameter

    Else:
    -> render request_result.html with error parameter as "unknown error"
    """
    if status is not None:
        return render(request, template_name='RequestManager/request_result.html',
                      context={"status": status})
    elif error is not None:
        return render(request, template_name='RequestManager/request_result.html',
                      context={"error": error})
    else:
        return render(request, template_name='RequestManager/request_result.html',
                      context={"error": "Unknown error"})


def updateDB(requestform):
    """
    Handle update of data to database

    Parameters
    ----------
    requestform : RequestForm
        The form which holds the new/edited information of the request

    Logic on priority
    ----------
        1. 1 is highest priority
        2. There is no maximum on priority
        Eg. you can have request of priority 1, 2 and 1000 of same client (the client says that 3rd one will be the last one they do)
        3. If you submit 1 request with the same priority number with the an existing request (same client),
        then the existing will be pushed back to lower priority until there is no overlapping of priority
        Eg. (1,2,3,4) -> Insert with priority 2 -> (1, 2(New Item), 3(Old:2), 4(Old:3), 5(Old:4)
            (1,2,3,5) -> Insert with priority 2 -> (1, 2(New Item), 3(Old:2), 4(Old:3), 5 (No change)
        4. If a request is deleted then the priority list will not be updated. There will be just an empty slot there (like 1,2,3,5 if 4 is deleted)
        5. If an item is edited and the prioriy changes then it will go thorugh the 3rd point

    """

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
    """
    Show all request page, render 'RequestManager/all_requests.html'

    Parameters
    ----------
    page : int
        The page of results
        As the amount of requests can be large, they are divided into pages, each page holds 12 items

    Return
    ----------
    Render the all_requests.html with correct page items
    """
    all_requests = list(Request.objects.all())
    paginator = Paginator(all_requests, 12)
    allData = paginator.get_page(page)
    return render(request, 'RequestManager/all_requests.html', {'allData': allData})


class RequestView(generic.DetailView):
    """
    Detail view of each request
    Make use of the generic.DetailView

    Return
    ----------
    Render the RequestManager/detail.html with correct page items
    """
    model = Request
    template_name = 'RequestManager/detail.html'
    context_object_name = 'request_item'


def about(request):
    """
    About page, just render 'about.html'
    """
    return render(request, 'about.html')
