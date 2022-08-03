import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import purchaseOrder, purchaseOrderItems, goodsReceivingNote, goodsReceivingNoteItems
from inventory.models import item, supplier

#Nodes and Filters
class purchaseOrderNode(DjangoObjectType):
    class Meta:
        model = purchaseOrder
        filter_fields = ['id', 'date', 'status']
        interfaces = (graphene.relay.Node, )

class purchaseOrderItemsNode(DjangoObjectType):
    class Meta:
        model = purchaseOrderItems
        filter_fields = ['id', 'purchaseOrder', 'item', 'quantity']
        interfaces = (graphene.relay.Node, )

class goodsReceivingNotesNode(DjangoObjectType):
    class Meta:
        model = goodsReceivingNote
        filter_fields = ['id', 'date', 'supplier']
        interfaces = (graphene.relay.Node, )

class goodsReceivingNoteItemsNode(DjangoObjectType):
    class Meta:
        model = goodsReceivingNoteItems
        filter_fields = ['id', 'goodsReceivingNote', 'item', 'quantity', 'unit_price']
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    purchaseOrder = graphene.Field(purchaseOrderNode, id=graphene.Int())
    all_purchaseOrders = DjangoFilterConnectionField(purchaseOrderNode)

    purchaseOrderItems = graphene.Field(purchaseOrderItemsNode, id=graphene.Int())
    all_purchaseOrderItems = DjangoFilterConnectionField(purchaseOrderItemsNode)

    goodsReceivingNote = graphene.Field(goodsReceivingNotesNode, id=graphene.Int())
    all_goodsReceivingNotes = DjangoFilterConnectionField(goodsReceivingNotesNode)
    
    goodsReceivingNoteItems = graphene.Field(goodsReceivingNoteItemsNode, id=graphene.Int())
    all_goodsReceivingNoteItems = DjangoFilterConnectionField(goodsReceivingNoteItemsNode)
    
    def resolve_purchaseOrder(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return purchaseOrder.objects.get(pk=id)

    def resolve_all_purchaseOrders(self, info, **kwargs):
        return purchaseOrder.objects.all()

    def resolve_purchaseOrderItems(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return purchaseOrderItems.objects.get(pk=id)

    def resolve_all_purchaseOrderItems(self, info, **kwargs):
        return purchaseOrderItems.objects.all()

    def resolve_goodsReceivingNote(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return goodsReceivingNote.objects.get(pk=id)

    def resolve_all_goodsReceivingNotes(self, info, **kwargs):
        return goodsReceivingNote.objects.all()

    def resolve_goodsReceivingNoteItems(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return goodsReceivingNoteItems.objects.get(pk=id)

    def resolve_all_goodsReceivingNoteItems(self, info, **kwargs):
        return goodsReceivingNoteItems.objects.all()
        

## Mutations

"""CRUD for purchaseOrder"""
class CreatePurchaseOrder(graphene.relay.ClientIDMutation):
    class input:
        created_by = graphene.ID()
        status = graphene.String()

    purchaseOrder = graphene.Field(purchaseOrderNode)

    def mutate(self, info, **input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        purchaseOrder = purchaseOrder(status=input.get('status'), created_by=user)
        purchaseOrder.save()

        return CreatePurchaseOrder(purchaseOrder=purchaseOrder)

class updatePurchaseOrder(graphene.Mutation):
    class input:
        id = graphene.ID()
        # supplier = graphene.String()
        status = graphene.String()

    purchaseOrder = graphene.Field(purchaseOrderNode)

    def mutate(self, info, **input):
        id=input.get('id')
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        purchaseOrder = purchaseOrder.objects.get(pk=id)
        # purchaseOrder.supplier = supplier
        purchaseOrder.status = input.get('status')
        purchaseOrder.save()

        return updatePurchaseOrder(purchaseOrder=purchaseOrder)

class deletePurchaseOrder(graphene.relay.ClientIDMutation):
    class input:
        id = graphene.Int()

    purchaseOrder = graphene.Field(purchaseOrderNode)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        purchaseOrder = purchaseOrder.objects.get(pk=id)
        purchaseOrder.delete()

        return deletePurchaseOrder(purchaseOrder=purchaseOrder)

"""CRUD for purchaseOrderItems"""

class CreatePurchaseOrderItems(graphene.Mutation):
    class input:
        purchaseOrder = graphene.ID()
        item = graphene.ID()
        quantity = graphene.Int()

    purchaseOrderItems = graphene.Field(purchaseOrderItemsNode)

    def mutate(self, info, **input):
        item = item.objects.get(pk=input.get('item'))
        purchaseOrder = purchaseOrder.objects.get(pk=input.get('purchaseOrder'))
        purchaseOrderItems = purchaseOrderItems(purchaseOrder=purchaseOrder, item=item, quantity=input.get('quantity'))
        purchaseOrderItems.save()

        return CreatePurchaseOrderItems(purchaseOrderItems=purchaseOrderItems)

class updatePurchaseOrderItems(graphene.Mutation):
    class input:
        id = graphene.ID()
        purchaseOrder = graphene.ID()
        item = graphene.ID()
        quantity = graphene.Int()

    purchaseOrderItems = graphene.Field(purchaseOrderItemsNode)

    def mutate(self, info, **input):
        id=input.get('id')
        item = item.objects.get(pk=input.get('item'))
        purchaseOrder = purchaseOrder.objects.get(pk=input.get('purchaseOrder'))
        purchaseOrderItems = purchaseOrderItems.objects.get(pk=id)
        purchaseOrderItems.purchaseOrder = purchaseOrder
        purchaseOrderItems.item = item
        purchaseOrderItems.quantity = input.get('quantity')
        purchaseOrderItems.save()

        return updatePurchaseOrderItems(purchaseOrderItems=purchaseOrderItems)
    
class deletePurchaseOrderItems(graphene.relay.ClientIDMutation):
    class input:
        id = graphene.Int()

    purchaseOrderItems = graphene.Field(purchaseOrderItemsNode)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        purchaseOrderItems = purchaseOrderItems.objects.get(pk=id)
        purchaseOrderItems.delete()

        return deletePurchaseOrderItems(purchaseOrderItems=purchaseOrderItems)

## CRUD for goodsReceivingNote

class CreateGoodsReceivingNote(graphene.relay.ClientIDMutation):
    class input:
        created_by = graphene.ID()
        supplier = graphene.ID()

    goodsReceivingNote = graphene.Field(goodsReceivingNotesNode)

    def mutate(self, info, **input):
        user = info.context.user
        supplier = supplier.objects.get(pk=input.get('supplier'))
        if user.is_anonymous:
            raise Exception('Not logged in!')
        goodsReceivingNote = goodsReceivingNote(supplier=supplier, created_by=user)
        goodsReceivingNote.save()

        return CreateGoodsReceivingNote(goodsReceivingNote=goodsReceivingNote)
    class input:
        created_by = graphene.ID()
        status = graphene.String()

    goodsReceivingNote = graphene.Field(goodsReceivingNotesNode)

class updateGoodsReceivingNote(graphene.Mutation):
    class input:
        id = graphene.ID()
        supplier = graphene.ID()
        status = graphene.String()

    goodsReceivingNote = graphene.Field(goodsReceivingNotesNode)

    def mutate(self, info, **input):
        id=input.get('id')
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        goodsReceivingNote = goodsReceivingNote.objects.get(pk=id)
        # goodsReceivingNote.supplier = supplier
        goodsReceivingNote.status = input.get('status')
        goodsReceivingNote.save()

        return updateGoodsReceivingNote(goodsReceivingNote=goodsReceivingNote)

class deleteGoodsReceivingNote(graphene.relay.ClientIDMutation):
    class input:
        id = graphene.Int()

    goodsReceivingNote = graphene.Field(goodsReceivingNotesNode)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        goodsReceivingNote = goodsReceivingNote.objects.get(pk=id)
        goodsReceivingNote.delete()

        return deleteGoodsReceivingNote(goodsReceivingNote=goodsReceivingNote)


## CRUD for goodsReceivingNoteItems

class CreateGoodsReceivingNoteItems(graphene.Mutation):
    class input:
        goodsReceivingNote = graphene.ID()
        item = graphene.ID()
        quantity = graphene.Int()
        unit_price = graphene.Float()
    goodsReceivingNoteItems = graphene.Field(goodsReceivingNoteItemsNode)

    def mutate(self, info, **input):
        item = item.objects.get(pk=input.get('item'))
        goodsReceivingNote = goodsReceivingNote.objects.get(pk=input.get('goodsReceivingNote'))
        goodsReceivingNoteItems = goodsReceivingNoteItems(goodsReceivingNote=goodsReceivingNote, item=item, quantity=input.get('quantity'), unit_price=input.get('unit_price'))
        goodsReceivingNoteItems.save()

        return CreateGoodsReceivingNoteItems(goodsReceivingNoteItems=goodsReceivingNoteItems)


class updateGoodsReceivingNoteItems(graphene.Mutation):
    class input:
        id = graphene.ID()
        goodsReceivingNote = graphene.ID()
        item = graphene.ID()
        quantity = graphene.Int()
        unit_price = graphene.Float()

    goodsReceivingNoteItems = graphene.Field(goodsReceivingNoteItemsNode)

    def mutate(self, info, **input):
        id=input.get('id')
        item = item.objects.get(pk=input.get('item'))
        goodsReceivingNote = goodsReceivingNote.objects.get(pk=input.get('goodsReceivingNote'))
        goodsReceivingNoteItems = goodsReceivingNoteItems.objects.get(pk=id)
        goodsReceivingNoteItems.goodsReceivingNote = goodsReceivingNote
        goodsReceivingNoteItems.item = item
        goodsReceivingNoteItems.quantity = input.get('quantity')
        goodsReceivingNoteItems.unit_price = input.get('unit_price')
        goodsReceivingNoteItems.save()

        return updateGoodsReceivingNoteItems(goodsReceivingNoteItems=goodsReceivingNoteItems)

class deleteGoodsReceivingNoteItem(graphene.relay.ClientIDMutation):
    class input:
        id = graphene.Int()

    goodsReceivingNoteItems = graphene.Field(goodsReceivingNoteItemsNode)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        goodsReceivingNoteItems = goodsReceivingNoteItems.objects.get(pk=id)
        goodsReceivingNoteItems.delete()

        return deleteGoodsReceivingNoteItem(goodsReceivingNoteItems=goodsReceivingNoteItems)

mutations = graphene.Mutation(
    createPurchaseOrder=CreatePurchaseOrder.Field(),
    updatePurchaseOrder=updatePurchaseOrder.Field(),
    deletePurchaseOrder=deletePurchaseOrder.Field(),

    createPurchaseOrderItems=CreatePurchaseOrderItems.Field(),
    updatePurchaseOrderItems=updatePurchaseOrderItems.Field(),
    deletePurchaseOrderItems=deletePurchaseOrderItems.Field(),

    createGoodsReceivingNote=CreateGoodsReceivingNote.Field(),
    updateGoodsReceivingNote=updateGoodsReceivingNote.Field(),
    deleteGoodsReceivingNote=deleteGoodsReceivingNote.Field(),

    createGoodsReceivingNoteItems=CreateGoodsReceivingNoteItems.Field(),
    updateGoodsReceivingNoteItems=updateGoodsReceivingNoteItems.Field(),
    deleteGoodsReceivingNoteItem=deleteGoodsReceivingNoteItem.Field(),
)





    