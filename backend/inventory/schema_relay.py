import email
from unicodedata import name
import graphene
from pkg_resources import require
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

#Mutations

''' CRUD for store '''
class createStore(graphene.ClientIDMutation):
    store = graphene.Field(storeNode)
    class Input:
        name = graphene.String()
    def mutate_and_get_payload(root, info, **input):
        Store = store(name=input.get('name'))
        Store.save()
        return createStore(store=Store)

class updateStore(graphene.ClientIDMutation):
    store = graphene.Field(storeNode)
    class Input:
        id = graphene.ID()
        name = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        Store = store.objects.get(id=input.get('id'))
        Store.name = input.get('name')
        Store.save()
        return updateStore(store=Store)
class deleteStore(graphene.ClientIDMutation):
    store = graphene.Field(storeNode)

    class Input:
        id = graphene.ID()
    
    def mutate_and_get_payload(root, info, **input):
        Store = store.objects.get(id=input.get('id'))
        Store.delete()
        return deleteStore(store=Store)

"""CRUD for supplier"""

class createSupplier(graphene.ClientIDMutation):
    supplier = graphene.Field(supplierNode)
    class Input:
        first_name=graphene.String(required=True)
        last_name=graphene.String(required=True)
        phone_number=graphene.String(required=True)
        email=graphene.String()
        address=graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        Supplier = supplier(first_name=input.get('first_name'),last_name=input.get('last_name'),phone_number=input.get('phone_number'),email=input.get('email'),address=input.get('address'))
        Supplier.save()
        return createSupplier(supplier=Supplier)

class updateSupplier(graphene.ClientIDMutation):
    supplier = graphene.Field(supplierNode)
    class Input:
        id = graphene.ID()
        first_name=graphene.String(required=True)
        last_name=graphene.String(required=True)
        phone_number=graphene.String(required=True)
        email=graphene.String()
        address=graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        Supplier = supplier.objects.get(id=input.get('id'))
        Supplier.first_name = input.get('first_name')
        Supplier.last_name = input.get('last_name')
        Supplier.phone_number = input.get('phone_number')
        Supplier.email = input.get('email')
        Supplier.address = input.get('address')
        Supplier.save()
        return updateSupplier(supplier=Supplier)

class deleteSupplier(graphene.ClientIDMutation):
    supplier = graphene.Field(supplierNode)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(root, info, **input):
        Supplier = supplier.objects.get(id=input.get('id'))
        Supplier.delete()
        return deleteSupplier(supplier=Supplier)

"""CRUD for item_category"""

class createItemCategory(graphene.ClientIDMutation):
    item_category = graphene.Field(itemCategoriesNode)

    class Input:
        name = graphene.String(required=True)
    
    def mutate_and_get_payload(root, info, **input):
        ItemCategory = item_category(name=input.get('name'))
        ItemCategory.save()
        return createItemCategory(item_category=ItemCategory)

class updateItemCategory(graphene.ClientIDMutation):
    item_category = graphene.Field(itemCategoriesNode)
    class Input:
        id = graphene.ID()
        name = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        ItemCategory = item_category.objects.get(id=input.get('id'))
        ItemCategory.name = input.get('name')
        ItemCategory.save()
        return updateItemCategory(item_category=ItemCategory)
class deleteItemCategory(graphene.ClientIDMutation):
    item_category = graphene.Field(itemCategoriesNode)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(root, info, **input):
        ItemCategory = item_category.objects.get(id=input.get('id'))
        ItemCategory.delete()
        return deleteItemCategory(item_category=ItemCategory)
"""CRUD for item"""
class createItem(graphene.ClientIDMutation):
    item = graphene.Field(itemNode)
    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        item_category = graphene.ID()
        price = graphene.Float(required=True)
        store = graphene.ID(required=True)
        supplier = graphene.ID(required=True)
        image = graphene.String()
        price=graphene.Float(required=True)
    
    

    def mutate_and_get_payload(root, info, **input):
        item_category_obj = item_category.objects.get(id=input.get('item_category'))
        supplier_obj = supplier.objects.get(id=input.get('supplier'))
        store_obj = store.objects.get(id=input.get('store'))

        Item = item(name=input.get('name'),description=input.get('description'),category=item_category_obj,price=input.get('price'),store=store_obj,supplier=supplier_obj,image=input.get('image'))
        Item.save()
        return createItem(item=Item)

class updateItem(graphene.ClientIDMutation):
    item = graphene.Field(itemNode)
    class Input:
        id = graphene.ID()
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        item_category = graphene.ID()
        price = graphene.Float(required=True)
        store = graphene.ID(required=True)
        supplier = graphene.ID(required=True)
        image = graphene.String()
        price=graphene.Float(required=True)
    
    def mutate_and_get_payload(root, info, **input):
        item_category_obj = item_category.objects.get(id=input.get('item_category'))
        supplier_obj = supplier.objects.get(id=input.get('supplier'))
        store_obj = store.objects.get(id=input.get('store'))

        Item = item.objects.get(id=input.get('id'))
        Item.name = input.get('name')
        Item.description = input.get('description')
        Item.category = item_category_obj
        Item.price = input.get('price')
        Item.store = store_obj
        Item.supplier = supplier_obj
        Item.image = input.get('image')
        Item.save()
        return updateItem(item=Item)

"""CRUD for merchandise transfer in"""

class createMerchandiseTransferIn(graphene.ClientIDMutation):
    merchandise_transfer_in = graphene.Field(merchandiseTransferInNode)
    class Input:
        store = graphene.ID(required=True)
        date = graphene.DateTime(required=True)
        total_price = graphene.Float(required=True)
        total_quantity = graphene.Int(required=True)



    def mutate_and_get_payload(root, info, **input):
        store_obj = store.objects.get(id=input.get('store'))
        
        MerchandiseTransferIn = merchandise_transfer_in(store=store_obj,date=input.get('date'),total_price=input.get('total_price'),total_quantity=input.get('total_quantity'))
        MerchandiseTransferIn.save()
        for item in input.get('items'):
            item_obj = item.objects.get(id=item)
            MerchandiseTransferIn.items.add(item_obj)
        return createMerchandiseTransferIn(merchandise_transfer_in=MerchandiseTransferIn)

class deleteItem(graphene.ClientIDMutation):
    item = graphene.Field(itemNode)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(root, info, **input):
        Item = item.objects.get(id=input.get('id'))
        Item.delete()
        return deleteItem(item=Item)

"""CRUD for wastage"""

class createWastage(graphene.ClientIDMutation):
    wastage = graphene.Field(wastageNode)
    class Input:
        date = graphene.DateTime() 
        quantity = graphene.Int(required=True)
        item = graphene.ID(required=True)       
        # store = graphene.ID(required=True)


    def mutate_and_get_payload(root, info, **input):
        # store_obj = store.objects.get(id=input.get('store'))
        item_obj = item.objects.get(id=input.get('item'))
        Wastage = wastage(date=input.get('date'), quantity=input.get('quantity'), item=item_obj)
        return createWastage(wastage=Wastage)

class updateWastage(graphene.ClientIDMutation):
    wastage = graphene.Field(wastageNode)
    class Input:
        id = graphene.ID()
        date = graphene.DateTime() 
        quantity = graphene.Int(required=True)
        item = graphene.ID(required=True)       
        # store = graphene.ID(required=True)

    def mutate_and_get_payload(root, info, **input):
        # store_obj = store.objects.get(id=input.get('store'))
        item_obj = item.objects.get(id=input.get('item'))
        Wastage = wastage.objects.get(id=input.get('id'))
        Wastage.date = input.get('date')
        Wastage.quantity = input.get('quantity')
        Wastage.item = item_obj
        Wastage.save()
        return updateWastage(wastage=Wastage)

class deleteWastage(graphene.ClientIDMutation):
    wastage = graphene.Field(wastageNode)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(root, info, **input):
        Wastage = wastage.objects.get(id=input.get('id'))
        Wastage.delete()
        return deleteWastage(wastage=Wastage)
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


class inventoryMutations(graphene.ObjectType):

    create_store = createStore.Field()
    update_store = updateStore.Field()
    delete_store = deleteStore.Field()

    create_supplier = createSupplier.Field()
    update_supplier = updateSupplier.Field()
    delete_supplier = deleteSupplier.Field()

    create_item= createItem.Field()
    update_item = updateItem.Field()
    delete_item = deleteItem.Field()


    create_wastage = createWastage.Field()