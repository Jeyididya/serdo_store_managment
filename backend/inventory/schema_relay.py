import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import *

class storeFilter(django_filters.FilterSet):
    class Meta:
        model = store
        fields = ['name']

class storeNode(DjangoObjectType):
    class Meta:
        model = store
        interfaces = (graphene.relay.Node,)

class supplierFilter(django_filters.FilterSet):
    class Meta:
        model = supplier
        fields = ['first_name', 'last_name']

class supplierNode(DjangoObjectType):
    class Meta:
        model = supplier
        interfaces = (graphene.relay.Node,)
class item_categoryFilter(django_filters.FilterSet):
    class Meta:
        model = item_category
        fields = ['name']
class itemCategoriesNode(DjangoObjectType):
    class Meta:
        model = item_category
        interfaces = (graphene.relay.Node,)
        
class itemFilter(django_filters.FilterSet):
    class Meta:
        model = item
        fields = ['name', 'category']

class itemNode(DjangoObjectType):
    class Meta:
        model = item
        interfaces = (graphene.relay.Node,)

class merchandiseTransferInFilter(django_filters.FilterSet):
    class Meta:
        model = merchandise_transfer_in
        fields = ['date','approved_by', 'received_by']

class merchandiseTransferInNode(DjangoObjectType):
    class Meta:
        model = merchandise_transfer_in
        interfaces = (graphene.relay.Node,)

class merchandiseTransferOutFilter(django_filters.FilterSet):
    class Meta:
        model = merchandise_transfer_out
        fields = ['date','approved_by']

class merchandiseTransferOutNode(DjangoObjectType):
    class Meta:
        model = merchandise_transfer_out
        interfaces = (graphene.relay.Node,)

class repairRequestFilter(django_filters.FilterSet):
    class Meta:
        model = repair_request
        fields = ['date','approved_by', 'status']

class repairRequestNode(DjangoObjectType):
    class Meta:
        model = repair_request
        interfaces = (graphene.relay.Node,)

class wastageFilter(django_filters.FilterSet):
    class Meta:
        model = wastage
        fields = ['date']

class wastageNode(DjangoObjectType):
    class Meta:
        model = wastage
        interfaces = (graphene.relay.Node,)

class inventoryQuery(graphene.ObjectType):
    relay_item = graphene.relay.Node.Field(itemNode)
    relay_items = DjangoFilterConnectionField(itemNode, filterset_class=itemFilter)
    relay_store = graphene.relay.Node.Field(storeNode)
    relay_stores = DjangoFilterConnectionField(storeNode, filterset_class=storeFilter)
    relay_supplier = graphene.relay.Node.Field(supplierNode)
    relay_suppliers = DjangoFilterConnectionField(supplierNode, filterset_class=supplierFilter)
    # relay_item_category = graphene.relay.Node.Field(itemCategoriesNode)
    relay_item_categories = DjangoFilterConnectionField(itemCategoriesNode, filterset_class=item_categoryFilter)
    relay_merchandise_transfer_in = graphene.relay.Node.Field(merchandiseTransferInNode)
    relay_merchandise_transfer_ins = DjangoFilterConnectionField(merchandiseTransferInNode, filterset_class=merchandiseTransferInFilter)
    relay_merchandise_transfer_out = graphene.relay.Node.Field(merchandiseTransferOutNode)
    relay_merchandise_transfer_outs = DjangoFilterConnectionField(merchandiseTransferOutNode, filterset_class=merchandiseTransferOutFilter)
    relay_repair_request = graphene.relay.Node.Field(repairRequestNode)
    relay_repair_requests = DjangoFilterConnectionField(repairRequestNode, filterset_class=repairRequestFilter)
    relay_wastage = graphene.relay.Node.Field(wastageNode)  
    relay_wastages = DjangoFilterConnectionField(wastageNode, filterset_class=wastageFilter)

