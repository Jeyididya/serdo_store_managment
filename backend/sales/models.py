from django.db import models
from django.utils.translation import gettext_lazy as _
from authentication.models import user
from inventory.models import item


class customer(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    address=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=10)
    email=models.EmailField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse("customer_detail", kwargs={"pk": self.pk})


class salesOrder(models.Model):
    item=models.ForeignKey(item,on_delete=models.CASCADE)
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    quantity=models.IntegerField(default=0)
    sales_person=models.ForeignKey(user,on_delete=models.CASCADE)
   
    class Meta:
        verbose_name = _("salesOrder")
        verbose_name_plural = _("salesOrders")

    def __str__(self):
        return self.customer.first_name + " " + self.customer.last_name

    def get_absolute_url(self):
        return reverse("salesOrder_detail", kwargs={"pk": self.pk})



class invoice(models.Model):
    sales_order=models.ForeignKey(salesOrder,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    paid_amount=models.FloatField()
    sales_person=models.ForeignKey(user,on_delete=models.CASCADE)
   
    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    def __str__(self):
        return self.sales_order.customer.first_name + " " + self.sales_order.customer.last_name

    def get_absolute_url(self):
        return reverse("invoice_detail", kwargs={"pk": self.pk})

