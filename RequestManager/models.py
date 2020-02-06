from django.db import models
from django.core.validators import MinValueValidator
from . import constants
# Create your models here.
class adminUser(models.Model):
    admin_email = models.EmailField(max_length=200, unique=True)
    admin_name = models.CharField(max_length=200)
    admin_password = models.CharField(max_length=200)

    def __str__(self):
        return '{}: {}'.format(self.admin_name, self.admin_email)


class ClientDetail(models.Model):
    client_name = models.CharField(max_length=200)
    request_amount = models.IntegerField(default=0)

    @property
    def get_request_amount(self):
        return self.request_amount

    def __str__(self):
        return self.client_name


class Request(models.Model):
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE)
    description = models.TextField(default="Please input description of the request")
    client_priority = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    submit_date = models.DateTimeField(auto_now=True)
    target_date = models.DateField('Target Date')
    product_area = models.IntegerField(choices=constants.PRODUCT_AREA, default=1)

    def __str__(self):
        return 'Priority {} from {}'.format(self.client_priority, self.client.client_name)


