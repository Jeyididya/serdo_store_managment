from django.contrib import admin
from .models import purchaseOrder, purchaseOrderItems, goodsReceivingNote, goodsReceivingNoteItems

admin.site.register(purchaseOrder)
admin.site.register(purchaseOrderItems)
admin.site.register(goodsReceivingNote)
admin.site.register(goodsReceivingNoteItems)