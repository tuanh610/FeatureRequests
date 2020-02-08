""" This file holds all the models that is used in the applications

For this assignment, there are 3 main models:
1. adminUser: store the information of admin users to be used for admin login (this has not been done)
2. clientDetail: store the information of clients which will be use as choice in the request
3. Request: store the information of each request

"""

from django.db import models
from django.core.validators import MinValueValidator
from . import constants


class adminUser(models.Model):
    """
    A class used to represent the admin user
    This will be used as a authentication method later
    ...

    Attributes
    ----------
    admin_email : models.EmailField
        the email of the admin, needs to be unique
    admin_name : models.CharField
        the name of the admin
    admin_password: models.CharField
        the password the admin
    """
    admin_email = models.EmailField(max_length=200, unique=True)
    admin_name = models.CharField(max_length=200)
    admin_password = models.CharField(max_length=200)

    def __str__(self):
        return '{}: {}'.format(self.admin_name, self.admin_email)


class ClientDetail(models.Model):
    """
    A class used to represent the client
    This will be used as choice in the Client field of each request
    ...

    Attributes
    ----------
    client_name : models.CharField
        The name of the client
    request_amount : models.IntegerField
        the amount of request for the client, this fields will be updated upon add/delete request
    """
    client_name = models.CharField(max_length=200)
    request_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.client_name


class Request(models.Model):
    """
        A class used to represent the request
        This will be used as choice in the Client field of each request
        ...

        Attributes
        ----------
        client : ClientDetail
            The owner of the request, link to ClientDetail model as a foreign key
        description : models.TextField
            Description of the request
        client_priority : models.PositiveIntegerField
            The priority of the request, highest is 1. The value should be unique, but this is handled in the view
            not as a property of the field
        submit_date : models.DateTimeField
            The time at which the report is submitted, this field is auto filled when the data is created
        target_date : models.DateField
            The date at which the request suppose to be finish
        product_area : models.IntegerField
            The area of the request, choices taken from the PRODUCT_AREA constants in the constants.py file
        """
    client = models.ForeignKey(ClientDetail, on_delete=models.CASCADE)
    description = models.TextField(default="Please input description of the request")
    client_priority = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    submit_date = models.DateTimeField(auto_now=True)
    target_date = models.DateField('Target Date')
    product_area = models.IntegerField(choices=constants.PRODUCT_AREA, default=1)

    def __str__(self):
        return 'Priority {} from {}'.format(self.client_priority, self.client.client_name)


