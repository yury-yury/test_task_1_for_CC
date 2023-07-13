from datetime import datetime
from typing import List
from django.db import models


class Node(models.Model):
    """
    The Node class inherits from the Model base class from the django.db.models module.
    Defines the fields of a database table, their properties and restrictions.
    """
    name = models.CharField(max_length=300, unique=True)
    supplier = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)
    level = models.IntegerField(choices=[(0, 0), (1, 1), (2, 2)])
    debt_to_the_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        The __str__ function overrides the method of the parent class Model and creates
        an output format for instances of this class.
        """
        return self.name

    class Meta:
        """
        The Meta class contains the common name of the model instance in the singular and plural used
        in the administration panel.
        """
        verbose_name: str = 'trading network member'
        verbose_name_plural: str = 'trading network members'
        ordering: List[str] = ['level']

    def save(self, *args, **kwargs):
        """
        The save function adds additional functionality to the method of the parent class. Automatically fills
        in fields when creating instances of the class. After that, it calls the method of the parent class.
        """
        if not self.id:
            self.date_of_creation = datetime.now()
        return super().save(*args, **kwargs)


class Contact(models.Model):
    """
    The Contact class inherits from the Model base class from the django.db.models module.
    Defines the fields of a database table, their properties and restrictions.
    """
    memder = models.OneToOneField(Node, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        """
        The Meta class contains the common name of the model instance in the singular and plural used
        in the administration panel.
        """
        verbose_name: str = 'contact'
        verbose_name_plural: str = 'contacts'


class Product(models.Model):
    """
    The Product class inherits from the Model base class from the django.db.models module.
    Defines the fields of a database table, their properties and restrictions.
    """
    name = models.CharField(max_length=150)
    model = models.CharField(max_length=100)
    release_date = models.DateField()
    owner = models.ForeignKey(Node, on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        """
        The __str__ function overrides the method of the parent class Model and creates
        an output format for instances of this class.
        """
        return self.name

    class Meta:
        """
        The Meta class contains the common name of the model instance in the singular and plural used
        in the administration panel.
        """
        verbose_name: str = 'product'
        verbose_name_plural: str = 'products'
        ordering: List[str] = ['name', 'model']

