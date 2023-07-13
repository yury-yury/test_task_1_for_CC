from typing import Tuple, List
from django.db import models
from rest_framework import serializers

from trade_network.models import Node, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model: models.Model = Contact
        fields: List[str] = ["email", "country", "city", "street", "house_number"]


class NodeCreateSerializer(serializers.ModelSerializer):
    """
        The NodeCreateSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
        This is a class for convenient serialization and deserialization of objects of the Node class when
        processing create new instance of Node class.
        """
    supplier = serializers.SlugRelatedField(required=False,
                                            queryset=Node.objects.all(),
                                            slug_field="name")
    contact = ContactSerializer(required=False)

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = Node
        read_only_fields: Tuple[str, ...] = ("id", "debt_to_the_supplier", "date_of_creation")
        fields: str = "__all__"

    def is_valid(self, *, raise_exception=False):
        self._contact = self.initial_data.pop("contact", [])
        self.initial_data["level"] = level_detection(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        node = Node.objects.create(**validated_data)
        node.save()

        contact = Contact.objects.create(memder_id=node,
                                         email=self._contact.get("email", None),
                                         country=self._contact.get("country", None),
                                         city=self._contact.get("city", None),
                                         street=self._contact.get("street", None),
                                         house_number=self._contact.get("house_number", None))
        contact.save()
        return node

def level_detection(kwargs):
    if kwargs["supplier"] is None:
        return 0
    else:
        supplier = Node.objects.get(name=kwargs["supplier"])
        if supplier.supplier is None:
            return 1
        return 2





