import re
from django.utils.translation import gettext_lazy as _
from django.db import models
from inventory.models import item, supplier
from authentication.models import user

class purchaseOrder(models.Model):
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, related_name='purchase_order_created_by')
    approved_by = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True, related_name='purchase_order_approved_by')
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=(('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')), default='Pending')
    def __str__(self):
        return str(self.id)

class purchaseOrderItems(models.Model):
    purchaseOrder = models.ForeignKey(purchaseOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(item, on_delete=models.CASCADE, related_name="purchase_order_item")
    quantity = models.IntegerField()
    def __str__(self):
        return str(self.id) +" " +str(self.purchaseOrder.date)


class goodsReceivingNote(models.Model):
    purchaser=models.ForeignKey(user, on_delete=models.CASCADE, related_name='goods_receiving_note_purchaser')
    date=models.DateField(auto_now_add=True)
    supplier=models.ForeignKey(supplier, on_delete=models.CASCADE, related_name='goods_receiving_note_supplier')

    class Meta:
        verbose_name = _("goods_receiving_note")
        verbose_name_plural = _("goods_receiving_notes")
    
    def __str__(self):
        return str(self.id) +" " +str(self.date) +" " +str(self.supplier.name)


class goodsReceivingNoteItems(models.Model):
    goodsReceivingNote = models.ForeignKey(goodsReceivingNote, on_delete=models.CASCADE)
    item = models.ForeignKey(item, on_delete=models.CASCADE, related_name="goods_receiving_note_item")
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id) +" " +str(self.goodsReceivingNote.date) +" " +str(self.item.name)

