from django.test import TestCase
from .models import store, supplier, item_category, item, merchandise_transfer_in,merchandise_transfer_out, merchandiseTransferInItem ,merchandiseTransferOutItem, wastage, repair_request
from authentication.models import user

#remaining
#   ->MerchandiseTransferIn
#   ->merchandiseTransferOut
#   ->merchandiseTransferOutItem
#  get_absolute_url()->for all models

class TestStore(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_store=store.objects.create(name="store 1")

    def test_model_str(self):
        self.assertEqual(str(self.test_store), "store 1")
    def test_get_absolute_url(self):
        pass
class TestSupplier(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_supplier=supplier.objects.create(first_name="fname",last_name="lname")

    def test_model_str(self):
        self.assertEqual(str(self.test_supplier), "fname lname")
    def test_get_absolute_url(self):
        pass


class TestItemCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_item_category=item_category.objects.create(name="item category1")

    def test_model_str(self):
        self.assertEqual(str(self.test_item_category), "item category1")
    def test_get_absolute_url(self):
        pass


class TestItem(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_item_category=item_category.objects.create(name="item category1")
        cls.test_store=store.objects.create(name="store 1")
        cls.test_supplier=supplier.objects.create(first_name="fname",last_name="lname")
        cls.test_item=item.objects.create(name="item 1",price=19.99,category=cls.test_item_category,store=cls.test_store,supplier=cls.test_supplier)

    def test_model_str(self):
        self.assertEqual(str(self.test_item), "item 1")
    def test_get_absolute_url(self):
        pass



class TestMerchandiseTransferInItem(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user=user.objects.create_user(username="user2",password="password")
        cls.test_store=store.objects.create(name="store 1")
        cls.test_merchandise_transfer_in=merchandise_transfer_in.objects.create(store=cls.test_store,approved_by=cls.test_user,received_by=cls.test_user)
           

        cls.test_item_category=item_category.objects.create(name="item category1")
        cls.test_store=store.objects.create(name="store 1")
        cls.test_supplier=supplier.objects.create(first_name="fname",last_name="lname")
        cls.test_item=item.objects.create(name="item 1",price=19.99,category=cls.test_item_category,store=cls.test_store,supplier=cls.test_supplier)
        cls.test_merchandiseTransferInItem=merchandiseTransferInItem.objects.create(item=cls.test_item, quantity=5, merchandise_transfer_in=cls.test_merchandise_transfer_in)

    def test_model_str(self):
        self.assertEqual(str(self.test_merchandiseTransferInItem), "item 1")
    def test_get_absolute_url(self):
        pass




class TestRepairRequest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_item_category=item_category.objects.create(name="item category1")
        cls.test_store=store.objects.create(name="store 1")
        cls.test_supplier=supplier.objects.create(first_name="fname",last_name="lname")
        cls.test_item=item.objects.create(name="item 1",price=19.99,category=cls.test_item_category,store=cls.test_store,supplier=cls.test_supplier)
        cls.test_user=user.objects.create(username="user 3", password="password3")
    
        
        cls.test_repair_request=repair_request.objects.create(item=cls.test_item,store=cls.test_store,requested_by=cls.test_user, approved_by=cls.test_user,quantity=19)

    def test_model_str(self):
        self.assertEqual(str(self.test_repair_request), "item 1 store 1")
    def test_get_absolute_url(self):
        pass


class TestWastage(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_item_category=item_category.objects.create(name="item category1")
        cls.test_store=store.objects.create(name="store 1")
        cls.test_supplier=supplier.objects.create(first_name="fname",last_name="lname")
        cls.test_item=item.objects.create(name="item 1",price=19.99,category=cls.test_item_category,store=cls.test_store,supplier=cls.test_supplier)

        cls.test_wastage=wastage.objects.create(item=cls.test_item,quantity=19.99)

    def test_model_str(self):
        self.assertEqual(str(self.test_wastage), "item 1 store 1")
    def test_get_absolute_url(self):
        pass