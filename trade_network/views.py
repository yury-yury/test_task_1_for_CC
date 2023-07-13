from typing import List

from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, serializers
from rest_framework.generics import CreateAPIView, ListAPIView

from trade_network.models import Node
from trade_network.serializers import NodeCreateSerializer, NodeListSerializer


class NodeCreateView(CreateAPIView):
    """
    The NodeCreateView class inherits from the CreateAPIView class from the rest_framework.generics module
    and is a class-based view for processing requests with POST methods at the address '/goals/goal_category/create'.
    """
    model: models.Model = Node
    # permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = NodeCreateSerializer


class NodeListView(ListAPIView):
    """

    """
    models: models.Model = Node
    # permission_classes: list = [permissions.IsAuthenticated]
    serializer_class: serializers.ModelSerializer = NodeListSerializer
    filter_backends: list = [DjangoFilterBackend,]
    filterset_fields: List[str] = ["country", ]


