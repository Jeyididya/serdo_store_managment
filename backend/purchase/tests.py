from django.test import TestCase
from .models import purchaseOrder, purchaseOrderItems, goodsReceivingNote, goodsReceivingNoteItems
from authentication.models import user
from inventory.models import item, store, item_category, supplier

#remaining
#  ->purchaseOrderItems
#  ->goodsReceivingNote
#  ->goodsReceivingNoteItems


class TestPurchaseOrder(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user=user.objects.create(username="user", password="password3")      
        cls.test_user2=user.objects.create(username="user 2", password="password3")      
        cls.test_purchase_order=purchaseOrder.objects.create(created_by=cls.test_user,approved_by=cls.test_user2)

    def test_model_str(self):
        self.assertEqual(str(self.test_purchase_order), "1")


# class TestPurchaseOrderItems(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_item_category=item_category.objects.create(name="item category1")
#         cls.test_store=store.objects.create(name="store 1")
#         cls.test_supplier=supplier.objects.create(first_name="fname",last_name="lname")
#         cls.test_item=item.objects.create(name="item 1",price=19.99,category=cls.test_item_category,store=cls.test_store,supplier=cls.test_supplier)

#         cls.test_user=user.objects.create(username="user", password="password3")      
#         cls.test_user2=user.objects.create(username="user 2", password="password3")      
#         cls.test_purchase_order=purchaseOrder.objects.create(created_by=cls.test_user,approved_by=cls.test_user2)

#         cls.test_purchase_order_item=purchaseOrderItems(item=cls.test_item,purchaseOrder=cls.test_purchase_order,quantity=19)


#     def test_model_str(self):
#         self.assertEqual(str(self.test_purchase_order_item), "1")  #date?
