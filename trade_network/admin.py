from typing import Tuple, List, Union
from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.utils.html import format_html

from trade_network.models import Node, Contact, Product


class ContactInline(admin.TabularInline):
    """
    The ContactInline class inherits from the TabularInline base class from the django.contrib.admin module.
    Designed to display and edit objects of related models on the same page of the Django.admin site
    as the object of the base model.
    """
    model: models.Model = Contact


class ProductInline(admin.TabularInline):
    """
    The ProductInline class inherits from the TabularInline base class from the django.contrib.admin module.
    Designed to display and edit objects of related models on the same page of the Django.admin site
    as the object of the base model.
    """
    model: models.Model = Product
    extra = 0


class NodeAdmin(admin.ModelAdmin):
    """
    The NodeAdmin class inherits from the ModelAdmin class. Defines the output of instance fields
    to the administration panel and the ability to edit them.
    """
    inlines: List[admin.TabularInline] = [ContactInline, ProductInline,]
    list_display: Tuple[str, ...] = ("id", "name", "level", "to_supplier", "debt_to_the_supplier")
    list_display_links: Tuple[str, ...] = ('name', 'to_supplier')
    list_filter: Tuple[str, ...] = ('contact__city', )
    fields: List[Union[Tuple[str, ...], str]] = [("id", "name"),
                                                 ("level", "supplier"),
                                                 "debt_to_the_supplier",
                                                 "date_of_creation"]
    readonly_fields: Tuple[str, ...] = ("id", "date_of_creation",)
    search_fields: Tuple[str, ...] = ("name",)
    save_on_top: bool = True
    actions: List[str] = ['clear_dept']

    def to_supplier(self, obj: Node):
        """
        The to_supplier function defines a method of the NodeAdmin class. It takes as arguments an instance
        of its own class and an instance of the Node class. Overrides the creation of a link in the list
        of instances on the Admin panel to the provider. Returns a link in html format.
        """
        if obj.supplier is not None:
            return format_html(
                '<a href="/admin/trade_network/node/{id}">{name}</a>',
                id=obj.supplier.id,
                name=obj.supplier
            )


    @admin.action(description='clear debt_to_the_supplier')
    def clear_dept(self, request, queryset: QuerySet) -> None:
        """
        The clear_dept(self, request, queryset: QuerySet function defines a method of the NodeAdmin class.
        It takes an instance of its own class, a request object, and a queryset object as arguments.
        Defines actions when the corresponding actions are selected in the Admin panel.
        """
        queryset.update(debt_to_the_supplier=0)


class ProductAdmin(admin.ModelAdmin):
    """
    The ProductAdmin class inherits from the ModelAdmin class. Defines the output of instance fields
    to the administration panel and the ability to edit them.
    """
    list_display: Tuple[str, ...] = ("name", "model", "release_date", "owner")
    list_display_links = ('name', 'owner')
    search_fields: Tuple[str, ...] = ("name", "model", "release_date")
    save_on_top = True


admin.site.register(Node, NodeAdmin)
admin.site.register(Product, ProductAdmin)

