from django.test import TestCase
from .models import store, supplier, item_category, item, merchandise_transfer_in,merchandise_transfer_out, merchandiseTransferInItem ,merchandiseTransferOutItem

# Create your tests here.

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
        cls.test_item=item.objects.create(name="item 1")

    def test_model_str(self):
        self.assertEqual(str(self.test_item), "item")
    def test_get_absolute_url(self):
        pass










# class TestMerchandiseTransferIn(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_store=store.objects.create(name="store 1")
#         cls.test_merchandise_transfer_in=merchandise_transfer_in.objects.create(store=cls.test_store,date="date")
            
#     def test_model_str(self):
#         self.assertEqual(str(self.test_merchandise_transfer_in), "Date store1") #date?
#     def test_get_absolute_url(self):
#         pass


# class TestMerchandiseTransferInItem(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_item_category=item_category.objects.create(name="item category1")
#         cls.test_item=item.objects.create(name="item 1",price=45,category=cls.test_item_category)
#         cls.test_merchandiseTransferInItem=merchandiseTransferInItem.objects.create(item=cls.test_item)

#     def test_model_str(self):
#         self.assertEqual(str(self.test_merchandiseTransferInItem), "merchandiseTransferInItem")
#     def test_get_absolute_url(self):
#         pass


# class TestMerchandiseTransferOut(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_merchandise_transfer_out=merchandise_transfer_out.objects.create(merchandise_transfer_out)

#     def test_model_str(self):
#         self.assertEqual(str(self.test_merchandise_transfer_out), "merchandise_transfer_out")
#     def test_get_absolute_url(self):
#         pass


# class TestMerchandiseTransferOutItem(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_merchandiseTransferOutItem=merchandiseTransferOutItem.objects.create(merchandiseTransferOutItem)

#     def test_model_str(self):
#         self.assertEqual(str(self.test_merchandiseTransferOutItem), "merchandiseTransferOutItem")
#     def test_get_absolute_url(self):
#         pass


# class TestRepairRequest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_repair_request=repair_request.objects.create(repair_request)

#     def test_model_str(self):
#         self.assertEqual(str(self.test_repair_request), "repair_request")
#     def test_get_absolute_url(self):
#         pass


# class TestWastage(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_wastage=wastage.objects.create(wastage)

#     def test_model_str(self):
#         self.assertEqual(str(self.test_wastage), "wastage")
#     def test_get_absolute_url(self):
#         pass