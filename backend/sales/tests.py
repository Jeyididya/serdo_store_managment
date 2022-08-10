from django.test import TestCase
from .models import customer, salesOrder, invoice
from authentication.models import user
from inventory.models import item, store, item_category, supplier


#remaining 
#   ->get_absolute_url() for all models

class TestCustomer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_customer=customer.objects.create(first_name="customer 1", last_name="lastname 1")            

    def test_model_str(self):
        self.assertEqual(str(self.test_customer), "customer 1 lastname 1")

class TestSalesOrder(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_customer=customer.objects.create(first_name="customer 1", last_name="lastname 1")            
        
        cls.test_item_category=item_category.objects.create(name="item category1")
        cls.test_store=store.objects.create(name="store 1")
        cls.test_supplier=supplier.objects.create(first_name="fname",last_name="lname")
        cls.test_item=item.objects.create(name="item 1",price=19.99,category=cls.test_item_category,store=cls.test_store,supplier=cls.test_supplier)

        cls.test_user=user.objects.create_user(username="username", password="password")

        cls.test_sales_order=salesOrder.objects.create(item=cls.test_item,customer=cls.test_customer,quantity=1,sales_person=cls.test_user)
    def test_model_str(self):
        self.assertEqual(str(self.test_sales_order), "customer 1 lastname 1")


class TestInvoice(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_customer=customer.objects.create(first_name="customer 1", last_name="lastname 1")            
        cls.test_item_category=item_category.objects.create(name="item category1")
        cls.test_store=store.objects.create(name="store 1")
        cls.test_supplier=supplier.objects.create(first_name="fname",last_name="lname")
        cls.test_item=item.objects.create(name="item 1",price=19.99,category=cls.test_item_category,store=cls.test_store,supplier=cls.test_supplier)
        cls.test_user=user.objects.create_user(username="username", password="password")
        cls.test_sales_order=salesOrder.objects.create(item=cls.test_item,customer=cls.test_customer,quantity=1,sales_person=cls.test_user)

        cls.test_invoice=invoice.objects.create(sales_order=cls.test_sales_order, sales_person=cls.test_user,paid_amount=19.99)

    def test_model_str(self):
        self.assertEqual(str(self.test_invoice), "customer 1 lastname 1")

