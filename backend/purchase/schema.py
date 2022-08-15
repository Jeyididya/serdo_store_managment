import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import purchaseOrder, purchaseOrderItems, goodsReceivingNote, goodsReceivingNoteItems
from inventory.models import item, supplier
from authentication.models import user

"""Purchase Order CRUD"""

class purchaseOrderFilter(django_filters.FilterSet):
    class Meta:
        model = purchaseOrder
        fields =['date', 'status']

class purchaseOrderNode(DjangoObjectType):
    class Meta:
        model = purchaseOrder
        interfaces = (graphene.relay.Node,)

class createPurchaseOrder(graphene.relay.ClientIDMutation):
    class Input:
        created_by = graphene.ID(required=True)
        approved_by = graphene.ID(required=False)
        date = graphene.Date(required=False)
        status = graphene.String(required=False)
    
    purchase_order = graphene.Field(purchaseOrderNode)
    
    def mutate_and_get_payload(root, info, **input):
        created_by = info.context.user
        approved_by = input.get('approved_by')
        if approved_by is not None:
            approved_by = user.objects.get(pk=approved_by)

        purchaseOrder.objects.create(
            created_by = created_by,
            approved_by = input.get('approved_by') or None,
            date = input.get('date'),
            status = input.get('status')
        )
        return createPurchaseOrder()

class updatePurchaseOrder(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        approved_by = graphene.ID(required=False)
        date = graphene.Date(required=False)
        status = graphene.String(required=False)

    purchase_order = graphene.Field(purchaseOrderNode)

    def mutate_and_get_payload(root, info, **input):
        approved_by = input.get('approved_by')
        if approved_by is not None:
            approved_by = user.objects.get(pk=approved_by)
        purchaseOrder.objects.filter(id=input.get('id')).update(
            approved_by = approved_by or None,
            date = input.get('date') or None,
            status = input.get('status') or None
        )
        return updatePurchaseOrder()

class deletePurchaseOrder(graphene.relay.ClientIDMutation):
    purchase_order = graphene.Field(purchaseOrderNode)
    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(root, info, **input):
        purchaseOrder.objects.filter(id=input.get('id')).delete()
        return deletePurchaseOrder()

"""Purchase Order Items CRUD"""

class purchaseOrderItemsFilter(django_filters.FilterSet):
    class Meta:
        model = purchaseOrderItems
        fields =['purchaseOrder', 'item', 'quantity']

class purchaseOrderItemsNode(DjangoObjectType):
    class Meta:
        model = purchaseOrderItems
        interfaces = (graphene.relay.Node,)

class createPurchaseOrderItems(graphene.relay.ClientIDMutation):
    class Input:
        purchaseOrder = graphene.ID(required=True)
        item = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    purchaseOrderItems = graphene.Field(purchaseOrderItemsNode)

    def mutate_and_get_payload(root, info, **input):
        item_instance = item.objects.get(pk=input.get('item')) 
        purchase_order_instance = purchaseOrder.objects.get(pk=input.get('purchaseOrder')) 
        instance = purchaseOrderItems.objects.create(item= item_instance, purchaseOrder=purchase_order_instance, quantity=input.get('quantity'))
        return createPurchaseOrderItems(purchaseOrderItems=instance)

class updatePurchaseOrderItems(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        purchaseOrder = graphene.ID()
        item = graphene.ID()
        quantity = graphene.Int()

    purchaseOrderItems = graphene.Field(purchaseOrderItemsNode)

    def mutate_and_get_payload(root, info, **input):
        instance = purchaseOrderItems.objects.get(pk=input.get('id'))
        purchaseOrder_instance = purchaseOrder.objects.get(pk=input.get('purchaseOrder'))
        item_instance = item.objects.get(pk=input.get('item'))
        instance.purchaseOrder = purchaseOrder_instance
        instance.item = item_instance
        instance.quantity = input.get('quantity')

        instance.save()
        return updatePurchaseOrderItems(purchaseOrderItems=instance)

class deletePurchaseOrderItems(graphene.relay.ClientIDMutation):
    purchaseOrderItems = graphene.Field(purchaseOrderItemsNode)
    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(root, info, **input):
        purchaseOrderItems.objects.filter(id=input.get('id')).delete()
        return deletePurchaseOrderItems()

"""Goods Receiving Note CRUD"""

class goodsReceivingNoteFilter(django_filters.FilterSet):
    class Meta:
        model = goodsReceivingNote
        fields =['date', 'supplier']

class goodsReceivingNoteNode(DjangoObjectType):
    class Meta:
        model = goodsReceivingNote
        interfaces = (graphene.relay.Node,)

class createGoodsReceivingNote(graphene.relay.ClientIDMutation):
    class Input:
        supplier = graphene.ID(required=True)

    goods_receiving_note = graphene.Field(goodsReceivingNoteNode)

    def mutate_and_get_payload(root, info, **input):
        purchaser = info.context.user
        print(purchaser)
        supplier_instance = supplier.objects.get(pk=input.get('supplier'))
        goodsReceivingNote.objects.create(
            purchaser = purchaser,
            supplier = supplier_instance
        )
        return createGoodsReceivingNote()

class updateGoodsReceivingNote(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        supplier = graphene.ID(required=False)

    goods_receiving_note = graphene.Field(goodsReceivingNoteNode)

    def mutate_and_get_payload(root, info, **input):
        supplier_instance = supplier.objects.get(pk=input.get('supplier'))
        goodsReceivingNote.objects.filter(id=input.get('id')).update(
            supplier = supplier_instance
        )
        return updateGoodsReceivingNote()

class deleteGoodsReceivingNote(graphene.relay.ClientIDMutation):
    goods_receiving_note = graphene.Field(goodsReceivingNoteNode)
    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(root, info, **input):
        goodsReceivingNote.objects.filter(id=input.get('id')).delete()
        return deleteGoodsReceivingNote()

"""Goods Receiving Note Items CRUD"""

class goodsReceivingNoteItemsFilter(django_filters.FilterSet):
    class Meta:
        model = goodsReceivingNoteItems
        fields =['goodsReceivingNote', 'item', 'quantity']

class goodsReceivingNoteItemsNode(DjangoObjectType):
    class Meta:
        model = goodsReceivingNoteItems
        interfaces = (graphene.relay.Node,)

class createGoodsReceivingNoteItems(graphene.relay.ClientIDMutation):
    class Input:
        goodsReceivingNote = graphene.ID(required=True)
        item = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    goodsReceivingNoteItems = graphene.Field(goodsReceivingNoteItemsNode)

    def mutate_and_get_payload(root, info, **input):
        item_instance = item.objects.get(pk=input.get('item')) 
        goods_receiving_note_instance = goodsReceivingNote.objects.get(pk=input.get('goodsReceivingNote')) 
        instance = goodsReceivingNoteItems.objects.create(item= item_instance, goodsReceivingNote=goods_receiving_note_instance, quantity=input.get('quantity'))
        return createGoodsReceivingNoteItems(goodsReceivingNoteItems=instance)

class updateGoodsReceivingNoteItems(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        goodsReceivingNote = graphene.ID()
        item = graphene.ID()
        quantity = graphene.Int()

    goodsReceivingNoteItems = graphene.Field(goodsReceivingNoteItemsNode)

    def mutate_and_get_payload(root,**input):
        instance = goodsReceivingNoteItems.objects.get(pk=input.get('id'))
        goodsReceivingNote_instance = goodsReceivingNote.objects.get(pk=input.get('goodsReceivingNote'))
        item_instance = item.objects.get(pk=input.get('item'))
        instance.goodsReceivingNote = goodsReceivingNote_instance
        instance.item = item_instance
        instance.quantity = input.get('quantity')

        instance.save()
        return updateGoodsReceivingNoteItems(goodsReceivingNoteItems=instance)

class deleteGoodsReceivingNoteItems(graphene.relay.ClientIDMutation):
    goodsReceivingNoteItems = graphene.Field(goodsReceivingNoteItemsNode)
    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(root, info, **input):
        goodsReceivingNoteItems.objects.filter(id=input.get('id')).delete()
        return deleteGoodsReceivingNoteItems()

class purchaseQuery(DjangoFilterConnectionField):
    purchase_order = graphene.relay.Node.Field(purchaseOrderNode)
    all_purchase_orders = DjangoFilterConnectionField(purchaseOrderNode, filterset_class=purchaseOrderFilter)

    purchase_order_items = graphene.relay.Node.Field(purchaseOrderItemsNode)
    all_purchase_order_items = DjangoFilterConnectionField(purchaseOrderItemsNode, filterset_class=purchaseOrderItemsFilter)

    goodsReceivingNote = graphene.relay.Node.Field(goodsReceivingNoteNode)
    all_goodsReceivingNotes = DjangoFilterConnectionField(goodsReceivingNoteNode, filterset_class=goodsReceivingNoteFilter)

class purchaseMutation(graphene.ObjectType):
    create_purchase_order=createPurchaseOrder.Field()
    update_purchase_order=updatePurchaseOrder.Field()
    delete_purchase_order=deletePurchaseOrder.Field()

    create_purchase_order_items=createPurchaseOrderItems.Field()
    update_purchase_order_items=updatePurchaseOrderItems.Field()
    delete_purchase_order_items=deletePurchaseOrderItems.Field()

    create_goods_receiving_note=createGoodsReceivingNote.Field()
    update_goods_receiving_note=updateGoodsReceivingNote.Field()
    delete_goods_receiving_note=deleteGoodsReceivingNote.Field()

    create_goods_receiving_note_items=createGoodsReceivingNoteItems.Field()
    update_goods_receiving_note_items=updateGoodsReceivingNoteItems.Field()
    delete_goods_receiving_note_items=deleteGoodsReceivingNoteItems.Field()