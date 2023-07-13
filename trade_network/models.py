from django.db import models
from django.db.models import SET_DEFAULT, CASCADE


class Node(models.Model):
    """

    """
    name = models.CharField(max_length=300, unique=True)
    supplier = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=SET_DEFAULT)
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

        """
        verbose_name = 'trading network member'
        verbose_name_plural = 'trading network members'
        ordering = ['level']


class Contact(models.Model):
    """

    """
    memder_id = models.OneToOneField(Node, on_delete=CASCADE)
    email = models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    house_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        """

        """
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'


class Product(models.Model):
    """

    """
    name = models.CharField(max_length=150)
    model = models.CharField(max_length=100)
    release_date = models.DateField()
    owner = models.ForeignKey(Node, on_delete=CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        """
        The __str__ function overrides the method of the parent class Model and creates
        an output format for instances of this class.
        """
        return self.name

    class Meta:
        """

        """
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['name', 'model']

