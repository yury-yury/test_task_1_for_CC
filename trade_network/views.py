from typing import List

from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, serializers
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from trade_network.models import Node
from trade_network.serializers import NodeCreateSerializer, NodeListSerializer, NodeSerializer


class NodeCreateView(CreateAPIView):
    """
    The NodeCreateView class inherits from the CreateAPIView class from the rest_framework.generics module
    and is a class-based view for processing requests with POST methods at the address '/goals/goal_category/create'.
    """
    model: models.Model = Node
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = NodeCreateSerializer


class NodeListView(ListAPIView):
    """

    """
    model: models.Model = Node
    queryset = Node.objects.all()
    permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = NodeListSerializer
    filter_backends: list = [DjangoFilterBackend,]
    filterset_fields: List[str] = ["contact__country", ]


class NodeView(RetrieveUpdateDestroyAPIView):
    """
    The NodeView class inherits from the RetrieveUpdateDestroyAPIView class from the rest_framework.generics
    module and is a class-based view for processing requests with GET, PUT, PATCH and DELETE methods at the address
    '/trade_network/node/<pk>'.
    """
    model: models.Model = Node
    queryset = Node.objects.all()
    serializer_class: serializers.ModelSerializer = NodeSerializer
    permission_classes: list = [permissions.IsAuthenticated,]
