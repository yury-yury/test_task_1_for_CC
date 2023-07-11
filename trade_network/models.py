from django.db import models


class Node(models.Model):
    """

    """
    name = models.CharField(max_length=300, unique=True)
    supplier = models.IntegerField(null=True)
    debt_to_the_supplier = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=10)

    def __str__(self) -> str:
        """
        The __str__ function overrides the method of the parent class Model and creates
        an output format for instances of this class.
        """
        return self.name

    class Meta:
        pass


class Product(models.Model):
    """

    """
    name = models.CharField(max_length=150)
    model = models.CharField(max_length=100)
    release_date = models.DateField()
    manufacturer = models.ManyToManyField(Node)

    def __str__(self) -> str:
        """
        The __str__ function overrides the method of the parent class Model and creates
        an output format for instances of this class.
        """
        return self.name
    class Meta:
        pass

