import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import *


"""Nodes and Filters for the Inventory Schema"""
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

class merchandiseTransferOutItemsFilter(django_filters.FilterSet):
    class Meta:
        model = merchandiseTransferOutItem
        fields = ['item']

class merchandiseTransferOutItemNode(DjangoObjectType):
    class Meta:
        model = merchandiseTransferOutItem
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

class merchandiseTransferInItemFilter(django_filters.FilterSet):
    class Meta:
        model = merchandiseTransferInItem
        fields = ['item']

class merchandiseTransferInItemNode(DjangoObjectType):
    class Meta:
        model = merchandiseTransferInItem
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

class deleteItem(graphene.ClientIDMutation):
    item = graphene.Field(itemNode)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(root, info, **input):
        Item = item.objects.get(id=input.get('id'))
        Item.delete()
        return deleteItem(item=Item)

"""CRUD for merchandise transfer in"""
class createMerchandiseTransferInItem(graphene.ClientIDMutation):
    merchandise_transfer_in_item = graphene.Field(merchandiseTransferInItemNode)
    class Input:
        item = graphene.ID(required=True)
        quantity = graphene.Int(required=True)
        price = graphene.Float(required=True)
        merchandise_transfer_in = graphene.ID(required=True)
    
    def mutate_and_get_payload(root, info, **input):
        item_obj = item.objects.get(id=input.get('item'))
        merchandise_transfer_in_obj = merchandise_transfer_in.objects.get(id=input.get('merchandise_transfer_in'))

        MerchandiseTransferInItem = merchandiseTransferInItem(item=item_obj,quantity=input.get('quantity'),price=input.get('price'),merchandise_transfer_in=merchandise_transfer_in_obj)
        MerchandiseTransferInItem.save()
        return createMerchandiseTransferInItem(merchandiseTransferInItem=MerchandiseTransferInItem)

class updateMerchandiseTransferInItem(graphene.ClientIDMutation):
    merchandise_transfer_in_item = graphene.Field(merchandiseTransferInItemNode)
    class Input:
        id = graphene.ID()
        item = graphene.ID(required=True)
        quantity = graphene.Int(required=True)
        price = graphene.Float(required=True)
        merchandise_transfer_in = graphene.ID(required=True)
    
    def mutate_and_get_payload(root, info, **input):
        item_obj = item.objects.get(id=input.get('item'))
        merchandise_transfer_in_obj = merchandise_transfer_in.objects.get(id=input.get('merchandise_transfer_in'))

        MerchandiseTransferInItem = merchandiseTransferInItem.objects.get(id=input.get('id'))
        MerchandiseTransferInItem.item = item_obj
        MerchandiseTransferInItem.quantity = input.get('quantity')
        MerchandiseTransferInItem.price = input.get('price')
        MerchandiseTransferInItem.merchandise_transfer_in = merchandise_transfer_in_obj
        MerchandiseTransferInItem.save()
        return updateMerchandiseTransferInItem(merchandiseTransferInItem=MerchandiseTransferInItem)

class deleteMerchandiseTransferInItem(graphene.ClientIDMutation):
    merchandise_transfer_in_item = graphene.Field(merchandiseTransferInItemNode)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(root, info, **input):
        MerchandiseTransferInItem = merchandiseTransferInItem.objects.get(id=input.get('id'))
        MerchandiseTransferInItem.delete()
        return deleteMerchandiseTransferInItem(merchandiseTransferInItem=MerchandiseTransferInItem)

class createMerchandiseTransferIn(graphene.ClientIDMutation):
    merchandise_transfer_in = graphene.Field(merchandiseTransferInNode)
    class Input:
        store = graphene.ID(required=True)
        # total_price = graphene.Float(required=True)
        status = graphene.String()
        approved_by = graphene.ID()      
    
    def mutate_and_get_payload(root, info, **input):
        store_obj = store.objects.get(id=input.get('store'))
        received_by = info.context.user
        MerchandiseTransferIn = merchandise_transfer_in(store=store_obj, received_by=received_by,status=input.get('status'), approved_by=input.get('approved_by'))
        MerchandiseTransferIn.save()
        return createMerchandiseTransferIn(merchandise_transfer_in=MerchandiseTransferIn)

class updateMerchandiseTransferIn(graphene.ClientIDMutation):
    merchandise_transfer_in = graphene.Field(merchandiseTransferInNode)
    class Input:
        id = graphene.ID()
        store = graphene.ID(required=True)
        # total_price = graphene.Float(required=True)
        status = graphene.String()
        approved_by = graphene.ID()
    
    def mutate_and_get_payload(root, info, **input):
        store_obj = store.objects.get(id=input.get('store'))
        supplier_obj = supplier.objects.get(id=input.get('supplier'))
        approved_by = user.objects.get(id=input.get('approved_by'))
        received_by = info.context.user

        MerchandiseTransferIn = merchandise_transfer_in.objects.get(id=input.get('id'))
        MerchandiseTransferIn.store = store_obj
        MerchandiseTransferIn.supplier = supplier_obj
        MerchandiseTransferIn.received_by = received_by
        MerchandiseTransferIn.status = input.get('status')
        MerchandiseTransferIn.approved_by = approved_by

        MerchandiseTransferIn.save()

        return updateMerchandiseTransferIn(merchandise_transfer_in=MerchandiseTransferIn)

class deleteMerchandiseTransferIn(graphene.ClientIDMutation):
    merchandise_transfer_in = graphene.Field(merchandiseTransferInNode)
    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(root, info, **input):
        MerchandiseTransferIn = merchandise_transfer_in.objects.get(id=input.get('id'))
        MerchandiseTransferIn.delete()
        return deleteMerchandiseTransferIn(merchandise_transfer_in=MerchandiseTransferIn)

"""CRUD for merchandise transfer out"""

class createMerchandiseTransferOutItem(graphene.ClientIDMutation):
    merchandise_transfer_out_item = graphene.Field(merchandiseTransferOutItemNode)
    class Input:
        item = graphene.ID(required=True)
        quantity = graphene.Int(required=True)
        # price = graphene.Float(required=True)
        merchandise_transfer_out = graphene.ID(required=True)
    
    def mutate_and_get_payload(root, info, **input):
        item_obj = item.objects.get(id=input.get('item'))
        merchandise_transfer_out_obj = merchandise_transfer_in.objects.get(id=input.get('merchandise_transfer_out'))

        MerchandiseTransferOutItem = merchandiseTransferInItem(item=item_obj,quantity=input.get('quantity'),merchandise_transfer_out=merchandise_transfer_out_obj)
        MerchandiseTransferOutItem.save()
        return createMerchandiseTransferOutItem(merchandiseTransferInItem=MerchandiseTransferOutItem)

class updateMerchandiseTransferOutItem(graphene.ClientIDMutation):
    merchandise_transfer_out_item = graphene.Field(merchandiseTransferOutItemNode)
    class Input:
        id = graphene.ID()
        item = graphene.ID(required=True)
        quantity = graphene.Int(required=True)
        # price = graphene.Float(required=True)
        merchandise_transfer_out = graphene.ID(required=True)
    
    def mutate_and_get_payload(root, info, **input):
        item_obj = item.objects.get(id=input.get('item'))
        merchandise_transfer_out_obj = merchandise_transfer_in.objects.get(id=input.get('merchandise_transfer_out'))

        MerchandiseTransferOutItem = merchandiseTransferOutItem.objects.get(id=input.get('id'))
        MerchandiseTransferOutItem.item = item_obj
        MerchandiseTransferOutItem.quantity = input.get('quantity')
        # MerchandiseTransferOutItem.price = input.get('price')
        MerchandiseTransferOutItem.merchandise_transfer_in = merchandise_transfer_out_obj
        MerchandiseTransferOutItem.save()
        return updateMerchandiseTransferOutItem(merchandiseTransferOutItem=MerchandiseTransferOutItem)

class deleteMerchandiseTransferOutItem(graphene.ClientIDMutation):
    merchandise_transfer_out_item = graphene.Field(merchandiseTransferOutItemNode)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(root, info, **input):
        MerchandiseTransferOutItem = merchandiseTransferOutItem.objects.get(id=input.get('id'))
        MerchandiseTransferOutItem.delete()
        return deleteMerchandiseTransferOutItem(merchandiseTransferInItem=MerchandiseTransferOutItem)

class createMerchandiseTransferOut(graphene.ClientIDMutation):
    merchandise_transfer_out = graphene.Field(merchandiseTransferOutNode)
    class Input:
        store = graphene.ID(required=True)
        # total_price = graphene.Float(required=True)
        status = graphene.String()
        approved_by = graphene.ID()      
    
    def mutate_and_get_payload(root, info, **input):
        store_obj = store.objects.get(id=input.get('store'))
        received_by = info.context.user
        MerchandiseTransferOut = merchandise_transfer_out(store=store_obj, received_by=received_by,status=input.get('status'), approved_by=input.get('approved_by'))
        MerchandiseTransferOut.save()
        return createMerchandiseTransferIn(merchandise_transfer_out=MerchandiseTransferOut)

class updateMerchandiseTransferOut(graphene.ClientIDMutation):
    merchandise_transfer_out = graphene.Field(merchandiseTransferOutNode)
    class Input:
        id = graphene.ID()
        store = graphene.ID(required=True)
        # total_price = graphene.Float(required=True)
        status = graphene.String()
        approved_by = graphene.ID()
    
    def mutate_and_get_payload(root, info, **input):
        store_obj = store.objects.get(id=input.get('store'))
        supplier_obj = supplier.objects.get(id=input.get('supplier'))
        approved_by = user.objects.get(id=input.get('approved_by'))
        received_by = info.context.user

        MerchandiseTransferOut = merchandise_transfer_out.objects.get(id=input.get('id'))
        MerchandiseTransferOut.store = store_obj
        MerchandiseTransferOut.supplier = supplier_obj
        MerchandiseTransferOut.received_by = received_by
        MerchandiseTransferOut.status = input.get('status')
        MerchandiseTransferOut.approved_by = approved_by

        MerchandiseTransferOut.save()

        return updateMerchandiseTransferIn(merchandise_transfer_out=MerchandiseTransferOut)

class deleteMerchandiseTransferOut(graphene.ClientIDMutation):
    merchandise_transfer_out = graphene.Field(merchandiseTransferOutNode)
    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(root, info, **input):
        MerchandiseTransferOut = merchandise_transfer_out.objects.get(id=input.get('id'))
        MerchandiseTransferOut.delete()
        return deleteMerchandiseTransferOut(merchandise_transfer_out=MerchandiseTransferOut)


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
    item = graphene.relay.Node.Field(itemNode)
    all_items = DjangoFilterConnectionField(itemNode, filterset_class=itemFilter)
    store = graphene.relay.Node.Field(storeNode)
    all_stores = DjangoFilterConnectionField(storeNode, filterset_class=storeFilter)
    supplier = graphene.relay.Node.Field(supplierNode)
    all_suppliers = DjangoFilterConnectionField(supplierNode, filterset_class=supplierFilter)
    item_category = graphene.relay.Node.Field(itemCategoriesNode)
    all_item_categories = DjangoFilterConnectionField(itemCategoriesNode, filterset_class=item_categoryFilter)
    merchandise_transfer_in = graphene.relay.Node.Field(merchandiseTransferInNode)
    all_merchandise_transfer_in = DjangoFilterConnectionField(merchandiseTransferInNode, filterset_class=merchandiseTransferInFilter)
    merchandise_transfer_out = graphene.relay.Node.Field(merchandiseTransferOutNode)
    all_merchandise_transfer_out = DjangoFilterConnectionField(merchandiseTransferOutNode, filterset_class=merchandiseTransferOutFilter)
    repair_request = graphene.relay.Node.Field(repairRequestNode)
    all_repair_requests = DjangoFilterConnectionField(repairRequestNode, filterset_class=repairRequestFilter)
    wastage = graphene.relay.Node.Field(wastageNode)  
    all_wastages = DjangoFilterConnectionField(wastageNode, filterset_class=wastageFilter)


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

    createMerchandiseTransferIn = createMerchandiseTransferIn.Field()