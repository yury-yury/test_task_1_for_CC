from typing import Tuple, List, Dict
from django.db import models
from rest_framework import serializers

from trade_network.models import Node, Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    The ContactSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Contact class when
    processing create new instance of Contact class.
    """
    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = Contact
        fields: List[str] = ["email", "country", "city", "street", "house_number"]


class NodeCreateSerializer(serializers.ModelSerializer):
    """
    The NodeCreateSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Node class when
    processing create new instance of Node class.
    """
    supplier = serializers.SlugRelatedField(required=False, queryset=Node.objects.all(), slug_field="name")
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
        """
        The is_valid function overrides the base class method. It takes as arguments an instance of its own class
        and any other positional arguments. Removes the "contact" key with a value from the received data
        and saves it as a protected attribute. Produces the addition of the "level" key with the value received
        from the function.It then calls the base class method.
        """
        self._contact: Dict[str, str] = self.initial_data.pop("contact", {})
        self.initial_data["level"] = level_detection(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data: dict) -> Node:
        """
        The create function overrides the base class method. It takes as arguments an instance of its own class
        and validated data received to create a new instance of the class. Creates and saves a new instance
        of the Node class. Creates and saves an instance of the associated Contact class.
        Returns the created instance of the Node class.
        """
        node: Node = Node.objects.create(**validated_data)
        node.save()

        contact: Contact = Contact.objects.create(
            memder=node,
            email=self._contact.get("email", None),
            country=self._contact.get("country", None),
            city=self._contact.get("city", None),
            street=self._contact.get("street", None),
            house_number=self._contact.get("house_number", None)
            )
        contact.save()

        return node


class NodeListSerializer(serializers.ModelSerializer):
    """
    The NodeListSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Node class when
    processing usage instance of Node class.
    """
    supplier = serializers.SlugRelatedField(queryset=Node.objects.all(), slug_field="name")
    contact = ContactSerializer()

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = Node
        fields: List[str] = ["id", "name", "level", "supplier", "debt_to_the_supplier", "contact"]


class NodeSerializer(serializers.ModelSerializer):
    """
    The NodeSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the Node class when
    processing usage instance of Node class.
    """
    supplier = serializers.SlugRelatedField(required=False, queryset=Node.objects.all(), slug_field="name")
    contact = ContactSerializer(required=False)

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model: models.Model = Node
        fields: str = "__all__"
        read_only_fields: Tuple[str, ...] = ("id", "debt_to_the_supplier", "date_of_creation", "level")

    def is_valid(self, *, raise_exception=False):
        """
        The is_valid function overrides the base class method. It takes as arguments an instance of its own class
        and any other positional arguments. Removes the "contact" key with a value from the received data
        and saves it as a protected attribute. Produces the addition of the "level" key with the value received
        from the function.It then calls the base class method.
        """
        self._contact = self.initial_data.pop("contact", {})
        if "supplier" in self.initial_data:
            self.initial_data["level"] = level_detection(self.initial_data)
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        """
        The save function overrides the base class method. It takes an instance of its own class as an argument.
        Calls the base class method. It then checks for data to change the associated instance of the Contact class.
        Updates and saves an instance of the associated Contact class. Returns an updated instance of the Node class.
        """
        super().save()

        if self._contact != {}:
            self.instance.contact = self.update(self.instance.contact, self._contact)

        return self.instance


def level_detection(kwargs: dict) -> int:
    """
    The level_detection function is a utility function. It takes as an argument data to create or update
    an instance of the Node class. Specifies the hierarchical level of the location of an instance of the Node class.
    Returns the level as an integer.
    """
    if kwargs["supplier"] is None:
        return 0
    else:
        supplier: Node = Node.objects.get(name=kwargs["supplier"])
        if supplier.supplier is None:
            return 1
        return 2





