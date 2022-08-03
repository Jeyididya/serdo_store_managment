from django.db import models
from PIL import Image
from django.utils.translation import gettext_lazy as _
from authentication.models import user

class store(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = _("store")
        verbose_name_plural = _("stores")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store_detail", kwargs={"pk": self.pk})


class supplier(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    address=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=10)
    email=models.EmailField(max_length=254, null=True, blank=True)


    class Meta:
        verbose_name = _("supplier")
        verbose_name_plural = _("suppliers")

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse("supplier_detail", kwargs={"pk": self.pk})


class item_category(models.Model):

    name=models.CharField(max_length=100)
    description=models.TextField()

    class Meta:
        verbose_name = _("item_category")
        verbose_name_plural = _("item_categories")

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("item_category_detail", kwargs={"pk": self.pk})

class item(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    category=models.ForeignKey(item_category,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    price=models.FloatField()
    selling_price=models.FloatField(default=0)
    image=models.ImageField(upload_to='media/item_images',blank=True)
    supplier=models.ForeignKey(supplier,on_delete=models.CASCADE) 
    store=models.ForeignKey(store,on_delete=models.CASCADE)
    date_registered=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})


class merchandise_transfer_in(models.Model):
    store=models.ForeignKey(store, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    received_by=models.ForeignKey(user, on_delete=models.CASCADE, related_name='received_by')
    approved_by=models.ForeignKey(user, on_delete=models.CASCADE, related_name='merchandise_in_approved_by', null=True, blank=True)
    status=models.CharField(max_length=10, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')))

    class Meta:
        verbose_name = _("merchandise_transfer_in")
    
    def __str__(self):
        return str(self.date) + " " + self.store.name
class merchandiseTransferInItem(models.Model):
    item=models.ForeignKey(item,on_delete=models.CASCADE, related_name="mtiv_item")
    quantity=models.IntegerField()
    merchandise_transfer_in=models.ForeignKey(merchandise_transfer_in,on_delete=models.CASCADE, related_name="mtiv_mti", null=True, blank=True)
    class Meta:
        verbose_name = _("merchandiseTransferItem")
        verbose_name_plural = _("merchandiseTransferItems")

    def __str__(self):
        return self.item.name
    def get_absolute_url(self):
        return reverse("merchandiseTransferItem_detail", kwargs={"pk": self.pk})

class merchandise_transfer_out(models.Model):
    store=models.ForeignKey(store, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    requested_by=models.ForeignKey(user, on_delete=models.CASCADE, related_name='requested_by')
    approved_by=models.ForeignKey(user, on_delete=models.CASCADE, related_name='approved_by', null=True, blank=True)
    status=models.CharField(max_length=10, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')), default='pending')

    class Meta:
        verbose_name = _("merchandise_transfer_out")
    
    def __str__(self):
        return self.item.__str__ + " " + self.store.name


class merchandiseTransferOutItem(models.Model):
    item=models.ForeignKey(item,on_delete=models.CASCADE, related_name="mtov_item")
    quantity=models.IntegerField()
    merchandise_transfer_out=models.ForeignKey(merchandise_transfer_out,on_delete=models.CASCADE, related_name="mtov_mti")
    class Meta:
        verbose_name = _("merchandiseTransferOutItem")
        verbose_name_plural = _("merchandiseTransferOutItems")

    def __str__(self):
        return self.item.name
    def get_absolute_url(self):
        return reverse("merchandiseTransferItem_detail", kwargs={"pk": self.pk})


class repair_request(models.Model):
    item=models.ForeignKey(item, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    store=models.ForeignKey(store, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    requested_by=models.ForeignKey(user, on_delete=models.CASCADE, related_name='repair_requested_by')
    approved_by=models.ForeignKey(user, on_delete=models.CASCADE, related_name='repair_approved_by')
    status=models.CharField(max_length=10, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')))

    class Meta:
        verbose_name = _("repair_request")
    
    def __str__(self):
        return self.item.name + " " + self.store.name


class wastage(models.Model):
    item=models.ForeignKey(item, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = _("wastage")
    
    def __str__(self):
        return self.item.name + " " + self.item.store.name
    

# class binCard(models.Model):
#     item=models.ForeignKey(item, on_delete=models.CASCADE)
#     quantity=models.IntegerField()
#     date=models.DateTimeField(auto_now_add=True)


#     class Meta:
#         verbose_name = _("binCard")
    
#     def __str__(self):
#         return self.item.name + " " + self.item.store.name