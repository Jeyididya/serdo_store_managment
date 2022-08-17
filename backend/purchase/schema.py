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

class purchaseOrderItemsInput(graphene.InputObjectType):
    item = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    price = graphene.Float(required=True)

class purchaseOrderMutation(graphene.relay.ClientIDMutation):
    purchaseOrder = graphene.Field(purchaseOrderNode)
    class Input:
        id = graphene.ID()
        approved_by = graphene.ID(required=False)
        status = graphene.String(required=True)
        purchaseOrderItems = graphene.List(purchaseOrderItemsInput)
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        if input.get('id'):
            purchase_order = purchaseOrder.objects.get(pk=input.get('id'))
        else:
            if input.get('approved_by'):
                approved_by = user.objects.get(pk=input.get('approved_by'))
            else:
                approved_by = None
            purchase_order = purchaseOrder.objects.create(
                status = input.get('status'),
                created_by = user,
                approved_by = approved_by
            )
            print(purchase_order)
        if input.get('purchaseOrderItems'):
            for purchaseOrderItem in input.get('purchaseOrderItems'):
                    purchaseOrderItems.objects.create(
                        item = item.objects.get(pk=purchaseOrderItem.get('item')),
                        quantity = purchaseOrderItem.get('quantity'),
                        price = purchaseOrderItem.get('price'),
                        purchaseOrder = purchase_order
                )
        return purchaseOrderMutation(purchaseOrder=purchase_order)

class deletePurchaseOrder(graphene.relay.ClientIDMutation):
    purchase_order = graphene.Field(purchaseOrderNode)
    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(root, info, **input):
        purchaseOrder.objects.filter(id=input.get('id')).delete()
        return deletePurchaseOrder()

"""Goods Receiving Note CRUD"""

class goodsReceivingNoteFilter(django_filters.FilterSet):
    class Meta:
        model = goodsReceivingNote
        fields =['date', 'supplier']

class goodsReceivingNoteNode(DjangoObjectType):
    class Meta:
        model = goodsReceivingNote
        interfaces = (graphene.relay.Node,)

class goodsReceivingNoteItemsInput(graphene.InputObjectType):
    item = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    unit_price = graphene.Float(required=True)


class goodsReceivingNoteMutation(graphene.relay.ClientIDMutation):
    goodsReceivingNote = graphene.Field(goodsReceivingNoteNode)
    class Input:
        id = graphene.ID()
        supplier = graphene.ID(required=True)
        goodsReceivingNoteItems = graphene.List(goodsReceivingNoteItemsInput)
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        if input.get('id'):
            goods_receiving_note = goodsReceivingNote.objects.get(pk=input.get('id'))
        else:
            goods_receiving_note = goodsReceivingNote.objects.create(
                supplier = supplier.objects.get(pk=input.get('supplier')),
                purchaser = user
            )
        if input.get('goodsReceivingNoteItems'):
            for goodsReceivingNoteItem in input.get('goodsReceivingNoteItems'):
                    goodsReceivingNoteItems.objects.create(
                        item = item.objects.get(pk=goodsReceivingNoteItem.get('item')),
                        quantity = goodsReceivingNoteItem.get('quantity'),
                        unit_price = goodsReceivingNoteItem.get('unit_price'),
                        goodsReceivingNote = goods_receiving_note
                )
        return goodsReceivingNoteMutation(goodsReceivingNote=goods_receiving_note)

class deleteGoodsReceivingNote(graphene.relay.ClientIDMutation):
    goods_receiving_note = graphene.Field(goodsReceivingNoteNode)
    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(root, info, **input):
        goodsReceivingNote.objects.filter(id=input.get('id')).delete()
        return deleteGoodsReceivingNote()

class purchaseQuery(DjangoFilterConnectionField):
    purchase_order = graphene.relay.Node.Field(purchaseOrderNode)
    all_purchase_orders = DjangoFilterConnectionField(purchaseOrderNode, filterset_class=purchaseOrderFilter)

    goodsReceivingNote = graphene.relay.Node.Field(goodsReceivingNoteNode)
    all_goodsReceivingNotes = DjangoFilterConnectionField(goodsReceivingNoteNode, filterset_class=goodsReceivingNoteFilter)

class purchaseMutation(graphene.ObjectType):
    create_purchase_order=purchaseOrderMutation.Field()
    delete_purchase_order=deletePurchaseOrder.Field()

    create_goods_receiving_note=goodsReceivingNoteMutation.Field()
    delete_goods_receiving_note=deleteGoodsReceivingNote.Field()