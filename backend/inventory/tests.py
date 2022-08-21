from django.test import TestCase,Client
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



import inventory.schema_relay as inventory_schema
import authentication.schema as authentication_schema
import graphene
# from django.contrib.auth import authenticate, login


"""store  graphene test"""
class TestCreateStore(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
    def test_mutate_and_get_payload(self):
        test_store=self.schema.execute(
            """
            mutation{
                createStore(input:{name:"store1"}){
                    store{
                        name,
                    }
                }
            }
            """
        )
        self.assertEqual(test_store.data['createStore']['store']['name'], "store1")

class TestUpdateStore(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
        cls.schema.execute(
            """
            mutation{
                createStore(input:{name:"store1"}){
                    store{
                        name,
                    }
                }
            }
            """
        )
    
    def test_mutate_and_get_payload(self):
        test_store=self.schema.execute(
            """
            mutation{
                updateStore(input:{id:1 name:"new_store_name"}){
                    store{
                        name,
                    }
                }
            }
            """
        )
        self.assertEqual(test_store.data['updateStore']['store']['name'], "new_store_name")

class TestDeleteStore(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
        cls.schema.execute(
            """
            mutation{
                createStore(input:{name:"store1"}){
                    store{
                        name,
                    }
                }
            }
            """
        )
    
    def test_mutate_and_get_payload(self):
        test_store=self.schema.execute(
            """
            mutation{
                deleteStore(input:{id:1}){
                    store{
                        name,
                    }
                }
            }
            """
        )
        self.assertEqual(test_store.data['deleteStore']['store']['name'], "store1")



"""supplier graphene test"""

class TestCreateSupplier(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
       
    
    def test_mutate_and_get_payload(self):
        test_supplier=self.schema.execute(
            """
           mutation{
            createSupplier(input:{firstName:"old_name",lastName:"old_lastname",phoneNumber:"0912852729",email:"xold@yold.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            }
            """
        )
        self.assertEqual(test_supplier.data['createSupplier']['supplier']['firstName'], "old_name")
        self.assertEqual(test_supplier.data['createSupplier']['supplier']['lastName'], "old_lastname")
        self.assertEqual(test_supplier.data['createSupplier']['supplier']['phoneNumber'], "0912852729")
        self.assertEqual(test_supplier.data['createSupplier']['supplier']['email'], "xold@yold.com")
        self.assertEqual(test_supplier.data['createSupplier']['supplier']['address'], "ayertena")



class TestUpdateSupplier(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
        cls.test_supplier=cls.schema.execute(
            """
           mutation{
            createSupplier(input:{firstName:"x",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            }
            """
        )
    
    def test_mutate_and_get_payload(self):
        test_supplier_=self.schema.execute(
            """
           mutation{
                updateSupplier(input:{id :1,firstName:"newname",lastName:"new_last_name",phoneNumber:"0912852729",email:"newx@newy.com",address:"megenagna"}){
                    supplier{
                        id,
                        firstName,
                        lastName,
                        phoneNumber,
                        email,
                        address,
                        
                    }
                }
            }
            """
        )
        self.assertEqual(test_supplier_.data['updateSupplier']['supplier']['firstName'], "newname")
        self.assertEqual(test_supplier_.data['updateSupplier']['supplier']['lastName'], "new_last_name")
        self.assertEqual(test_supplier_.data['updateSupplier']['supplier']['phoneNumber'], "0912852729")
        self.assertEqual(test_supplier_.data['updateSupplier']['supplier']['email'], "newx@newy.com")
        self.assertEqual(test_supplier_.data['updateSupplier']['supplier']['address'], "megenagna")


class TestDeleteSupplier(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
        cls.test_supplier=cls.schema.execute(
            """
           mutation{
            createSupplier(input:{firstName:"x",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            }
            """
        )
    
    def test_mutate_and_get_payload(self):
        test_supplier_=self.schema.execute(
            """
           mutation{
                deleteSupplier(input:{id:1}){
                    supplier{
                        id,
                        firstName,
                        lastName,
                        phoneNumber,
                        email,
                        address,
                        
                    }
                }
            }
            """
        )
        self.assertEqual(test_supplier_.data['deleteSupplier']['supplier']['firstName'], "x")
        self.assertEqual(test_supplier_.data['deleteSupplier']['supplier']['lastName'], "y")
        self.assertEqual(test_supplier_.data['deleteSupplier']['supplier']['phoneNumber'], "0913129381")
        self.assertEqual(test_supplier_.data['deleteSupplier']['supplier']['email'], "x@y.com")
        self.assertEqual(test_supplier_.data['deleteSupplier']['supplier']['address'], "ayertena")






"""item_catagory graphene test"""
class TestCreateItemCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
       
    
    def test_mutate_and_get_payload(self):
        test_category=self.schema.execute(
            """
           mutation{
            createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }
            }
            """
        )
        self.assertEqual(test_category.data['createItemCategory']['itemCategory']['name'], "electronics")

class TestUpdateItemCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
        cls.test_category=cls.schema.execute(
            """
           mutation{
            createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }
            }
            """
        )
    
    def test_mutate_and_get_payload(self):
        test_category_=self.schema.execute(
            """
           mutation{
            updateItemCategory(input:{id:1, name:"furniture"}){
                itemCategory{
                    name,
                }
                }
            }
            """
        )
        self.assertEqual(test_category_.data['updateItemCategory']['itemCategory']['name'], "furniture")


class TestDeleteItemCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
        cls.test_category=cls.schema.execute(
            """
           mutation{
            createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }
            }
            """
        )
    
    def test_mutate_and_get_payload(self):
        test_category_=self.schema.execute(
            """
           mutation{
            deleteItemCategory(input:{id:1}){
                itemCategory{
                    name,
                }
                }
            }
            """
        )
        self.assertEqual(test_category_.data['deleteItemCategory']['itemCategory']['name'], "electronics")






"""item  graphene test"""


class TestCreateItem(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
        cls.test_item=cls.schema.execute(
            """
           mutation{
            createStore(input:{name:"store1"}){
                store{
                    name,
                }
            }
            
            createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }

            createSupplier(input:{firstName:"supplier_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            }
            """
        )
    
    def test_mutate_and_get_payload(self):
        test_item_=self.schema.execute(
            """
           mutation{
                createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1222,store:1,supplier:1,image:"not_avial"}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        self.assertEqual(test_item_.data['createItem']['item']['name'], "Phone")
        self.assertEqual(test_item_.data['createItem']['item']['description'], "mobile")
        self.assertEqual(test_item_.data['createItem']['item']['category']['name'], "electronics")
        self.assertEqual(test_item_.data['createItem']['item']['price'], 1222)
        self.assertEqual(test_item_.data['createItem']['item']['store']['name'], "store1")
        self.assertEqual(test_item_.data['createItem']['item']['supplier']['firstName'], "supplier_first_name")
        self.assertEqual(test_item_.data['createItem']['item']['image'], "not_avial")


class TestUpdateItem(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
        cls.test_item=cls.schema.execute(
            """
           mutation{
            createStore(input:{name:"store1"}){
                store{
                    name,
                }
            }
            
            createItemCategory(input:{name:"furniture"}){
                itemCategory{
                    name,
                }
            }

            createSupplier(input:{firstName:"supplier2_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1333,store:1,supplier:1,image:"not_avial"}){
                item{
                    name,
                    description,
                    category{
                    name,
                    },
                    price,
                    store{
                    name,
                    },
                    supplier{
                    firstName
                    },
                    image,
                }
            }


            }
            """
        )
    
    def test_mutate_and_get_payload(self):
        test_item_=self.schema.execute(
            """
           mutation{
                updateItem(input:{id:1,name:"PhoneCase",description:"mobile_phone",itemCategory:1,price:1333,store:1,supplier:1,image:"not_avial"}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        self.assertEqual(test_item_.data['updateItem']['item']['name'], "PhoneCase")
        self.assertEqual(test_item_.data['updateItem']['item']['description'], "mobile_phone")
        self.assertEqual(test_item_.data['updateItem']['item']['category']['name'], "furniture")
        self.assertEqual(test_item_.data['updateItem']['item']['price'], 1333)
        self.assertEqual(test_item_.data['updateItem']['item']['store']['name'], "store1")
        self.assertEqual(test_item_.data['updateItem']['item']['supplier']['firstName'], "supplier2_first_name")
        self.assertEqual(test_item_.data['updateItem']['item']['image'], "not_avial")






class TestDeleteItem(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.schema = graphene.Schema(query=inventory_schema.inventoryQuery, mutation=inventory_schema.inventoryMutations)
        cls.test_item=cls.schema.execute(
            """
           mutation{
            createStore(input:{name:"store1"}){
                store{
                    name,
                }
            }
            
            createItemCategory(input:{name:"furniture"}){
                itemCategory{
                    name,
                }
            }

            createSupplier(input:{firstName:"supplier2_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1333,store:1,supplier:1,image:"not_avial"}){
                item{
                    name,
                    description,
                    category{
                    name,
                    },
                    price,
                    store{
                    name,
                    },
                    supplier{
                    firstName
                    },
                    image,
                }
            }


            }
            """
        )
        
    
    def test_mutate_and_get_payload(self):
        test_item_=self.schema.execute(
            """
           mutation{
                deleteItem(input:{id:1}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        self.assertEqual(test_item_.data['deleteItem']['item']['name'], "Phone")
        self.assertEqual(test_item_.data['deleteItem']['item']['description'], "mobile")
        self.assertEqual(test_item_.data['deleteItem']['item']['category']['name'], "furniture")
        self.assertEqual(test_item_.data['deleteItem']['item']['price'], 1333)
        self.assertEqual(test_item_.data['deleteItem']['item']['store']['name'], "store1")
        self.assertEqual(test_item_.data['deleteItem']['item']['supplier']['firstName'], "supplier2_first_name")
        self.assertEqual(test_item_.data['deleteItem']['item']['image'], "not_avial")








"""trnafer in  graphene test"""

import core.schema as core_schema


from django.test import RequestFactory, TestCase
from graphene.test import Client as Cl

def execute_test_client_api_query(api_query, user=None, variable_values=None, **kwargs):
    """
    Returns the results of executing a graphQL query using the graphene test client.  This is a helper method for our tests
    """
    request_factory = RequestFactory()
    context_value = request_factory.get('/api/')  # or use reverse() on your API endpoint
    context_value.user = user
    cli = Cl(core_schema.schema)
    executed = cli.execute(api_query, context_value=context_value, variable_values=variable_values, **kwargs)
    return executed


class TestCreateTransferIn(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store1"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }
            }
            """
        )
        # print("-->",cls.test_item.data)
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferIn(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferIn{
                        status,
                        store{
                            name
                        },
                        receivedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            
            }
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",data)
        self.assertEqual(test_item_['createMerchandiseTransferIn']['merchandiseTransferIn']['status'], "APPROVED")
        self.assertEqual(test_item_['createMerchandiseTransferIn']['merchandiseTransferIn']['store']['name'], "store1")
        self.assertEqual(test_item_['createMerchandiseTransferIn']['merchandiseTransferIn']['receivedBy']['username'], "user2")
        self.assertEqual(test_item_['createMerchandiseTransferIn']['merchandiseTransferIn']['approvedBy']['username'], "user1")



class TestDeleteTransferIn(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferIn(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferIn{
                        status,
                        store{
                            name
                        },
                        receivedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                 deleteMerchandiseTransferIn(input:{id:1}){
                    merchandiseTransferIn{
                        status,
                        store{
                            name
                        },
                        receivedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            }
            
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['deleteMerchandiseTransferIn']['merchandiseTransferIn']['status'], "APPROVED")
        self.assertEqual(test_item_['deleteMerchandiseTransferIn']['merchandiseTransferIn']['store']['name'], "store2")
        self.assertEqual(test_item_['deleteMerchandiseTransferIn']['merchandiseTransferIn']['receivedBy']['username'], "user2")
        self.assertEqual(test_item_['deleteMerchandiseTransferIn']['merchandiseTransferIn']['approvedBy']['username'], "user1")




class TestUpdateTransferIn(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferIn(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferIn{
                        status,
                        store{
                            name
                        },
                        receivedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                 updateMerchandiseTransferIn(input:{id:1,approvedBy:1,status:"pending",store:1}){
                    merchandiseTransferIn{
                        status,
                        store{
                            name
                        },
                        receivedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            }
            
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['updateMerchandiseTransferIn']['merchandiseTransferIn']['status'], "PENDING")
        self.assertEqual(test_item_['updateMerchandiseTransferIn']['merchandiseTransferIn']['store']['name'], "store2")
        self.assertEqual(test_item_['updateMerchandiseTransferIn']['merchandiseTransferIn']['receivedBy']['username'], "user2")
        self.assertEqual(test_item_['updateMerchandiseTransferIn']['merchandiseTransferIn']['approvedBy']['username'], "user1")





""" transfer out test"""

class TestCreateTransferOut(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store1"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }
            }
            """
        )
        # print("-->",cls.test_item.data)
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferOut(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferOut{
                        status,
                        store{
                            name
                        },
                        requestedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            }
        
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['createMerchandiseTransferOut']['merchandiseTransferOut']['status'], "APPROVED")
        self.assertEqual(test_item_['createMerchandiseTransferOut']['merchandiseTransferOut']['store']['name'], "store1")
        self.assertEqual(test_item_['createMerchandiseTransferOut']['merchandiseTransferOut']['requestedBy']['username'], "user2")
        self.assertEqual(test_item_['createMerchandiseTransferOut']['merchandiseTransferOut']['approvedBy']['username'], "user1")



class TestUpdateTransferOut(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferOut(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferOut{
                        status,
                        store{
                            name
                        },
                        requestedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                 updateMerchandiseTransferOut(input:{id:1,approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferOut{
                        status,
                        store{
                            name
                        },
                        requestedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            }
            
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['updateMerchandiseTransferOut']['merchandiseTransferOut']['status'], "APPROVED")
        self.assertEqual(test_item_['updateMerchandiseTransferOut']['merchandiseTransferOut']['store']['name'], "store2")
        self.assertEqual(test_item_['updateMerchandiseTransferOut']['merchandiseTransferOut']['requestedBy']['username'], "user2")
        self.assertEqual(test_item_['updateMerchandiseTransferOut']['merchandiseTransferOut']['approvedBy']['username'], "user1")



class TestDeleteTransferOut(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferOut(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferOut{
                        status,
                        store{
                            name
                        },
                        requestedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                 deleteMerchandiseTransferOut(input:{id:1}){
                    merchandiseTransferOut{
                        status,
                        store{
                            name
                        },
                        requestedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            }
            
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['deleteMerchandiseTransferOut']['merchandiseTransferOut']['status'], "APPROVED")
        self.assertEqual(test_item_['deleteMerchandiseTransferOut']['merchandiseTransferOut']['store']['name'], "store2")
        self.assertEqual(test_item_['deleteMerchandiseTransferOut']['merchandiseTransferOut']['requestedBy']['username'], "user2")
        self.assertEqual(test_item_['deleteMerchandiseTransferOut']['merchandiseTransferOut']['approvedBy']['username'], "user1")




"""transfer initem  graphene test"""
class TestCreateMerchandiseTransferInItem(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }

                createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }

            createSupplier(input:{firstName:"supplier_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1222,store:1,supplier:1,image:"not_avial"}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferIn(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferIn{
                        status,
                        store{
                            name
                        },
                        receivedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferInItem(input:{item:1,quantity:3,merchandiseTransferIn:1}){
                    merchandiseTransferInItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferIn{
                        approvedBy {
                        username
                        },
                        receivedBy {
                        username
                        },
                    }
                    }
                }
            }
            
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['createMerchandiseTransferInItem']['merchandiseTransferInItem']['item']['name'], "Phone")
        self.assertEqual(test_item_['createMerchandiseTransferInItem']['merchandiseTransferInItem']['item']['description'], "mobile")
        self.assertEqual(test_item_['createMerchandiseTransferInItem']['merchandiseTransferInItem']['quantity'], 3)
        self.assertEqual(test_item_['createMerchandiseTransferInItem']['merchandiseTransferInItem']['merchandiseTransferIn']['approvedBy']['username'], "user1")





class TestUpdateMerchandiseTransferInItem(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }

                createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }

            createSupplier(input:{firstName:"supplier_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1222,store:1,supplier:1,image:"not_avial"}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferIn(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferIn{
                        status,
                        store{
                            name
                        },
                        receivedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
                createMerchandiseTransferInItem(input:{item:1,quantity:3,merchandiseTransferIn:1}){
                    merchandiseTransferInItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferIn{
                        approvedBy {
                        username
                        },
                        receivedBy {
                        username
                        },
                    }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                updateMerchandiseTransferInItem(input:{id:1,item:1,quantity:5,merchandiseTransferIn:1}){
                    merchandiseTransferInItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferIn{
                        approvedBy {
                        username
                        },
                        receivedBy {
                        username
                        },
                    }
                    }
                }
                
            }
            
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['updateMerchandiseTransferInItem']['merchandiseTransferInItem']['item']['name'], "Phone")
        self.assertEqual(test_item_['updateMerchandiseTransferInItem']['merchandiseTransferInItem']['item']['description'], "mobile")
        self.assertEqual(test_item_['updateMerchandiseTransferInItem']['merchandiseTransferInItem']['quantity'], 5)
        self.assertEqual(test_item_['updateMerchandiseTransferInItem']['merchandiseTransferInItem']['merchandiseTransferIn']['approvedBy']['username'], "user1")




class TestDeleteMerchandiseTransferInItem(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }

                createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }

            createSupplier(input:{firstName:"supplier_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1222,store:1,supplier:1,image:"not_avial"}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferIn(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferIn{
                        status,
                        store{
                            name
                        },
                        receivedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
                createMerchandiseTransferInItem(input:{item:1,quantity:3,merchandiseTransferIn:1}){
                    merchandiseTransferInItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferIn{
                        approvedBy {
                        username
                        },
                        receivedBy {
                        username
                        },
                    }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                deleteMerchandiseTransferInItem(input:{id:1}){
                    merchandiseTransferInItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferIn{
                        approvedBy {
                        username
                        },
                        receivedBy {
                        username
                        },
                    }
                    }
                }
                
            }
            
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['deleteMerchandiseTransferInItem']['merchandiseTransferInItem']['item']['name'], "Phone")
        self.assertEqual(test_item_['deleteMerchandiseTransferInItem']['merchandiseTransferInItem']['item']['description'], "mobile")
        self.assertEqual(test_item_['deleteMerchandiseTransferInItem']['merchandiseTransferInItem']['quantity'], 3)
        self.assertEqual(test_item_['deleteMerchandiseTransferInItem']['merchandiseTransferInItem']['merchandiseTransferIn']['approvedBy']['username'], "user1")





class TestCreateMerchandiseTransferOutItem(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }

                createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }

            createSupplier(input:{firstName:"supplier_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1222,store:1,supplier:1,image:"not_avial"}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferOut(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferOut{
                        status,
                        store{
                            name
                        },
                        requestedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferOutItem(input:{item:1,quantity:3,merchandiseTransferOut:1}){
                    merchandiseTransferOutItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferOut{
                        approvedBy {
                        username
                        },
                        requestedBy {
                        username
                        },
                    }
                    }
                }
            }
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['createMerchandiseTransferOutItem']['merchandiseTransferOutItem']['item']['name'], "Phone")
        self.assertEqual(test_item_['createMerchandiseTransferOutItem']['merchandiseTransferOutItem']['item']['description'], "mobile")
        self.assertEqual(test_item_['createMerchandiseTransferOutItem']['merchandiseTransferOutItem']['quantity'], 3)
        self.assertEqual(test_item_['createMerchandiseTransferOutItem']['merchandiseTransferOutItem']['merchandiseTransferOut']['approvedBy']['username'], "user1")





class TestUpdateMerchandiseTransferOutItem(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }

                createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }

            createSupplier(input:{firstName:"supplier_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1222,store:1,supplier:1,image:"not_avial"}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferOut(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferOut{
                        status,
                        store{
                            name
                        },
                        requestedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
                createMerchandiseTransferOutItem(input:{item:1,quantity:3,merchandiseTransferOut:1}){
                    merchandiseTransferOutItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferOut{
                        approvedBy {
                        username
                        },
                        requestedBy {
                        username
                        },
                    }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                updateMerchandiseTransferOutItem(input:{id:1,item:1,quantity:5,merchandiseTransferOut:1}){
                    merchandiseTransferOutItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferOut{
                        approvedBy {
                        username
                        },
                        requestedBy {
                        username
                        },
                    }
                    }
                }
                
            }
            
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['updateMerchandiseTransferOutItem']['merchandiseTransferOutItem']['item']['name'], "Phone")
        self.assertEqual(test_item_['updateMerchandiseTransferOutItem']['merchandiseTransferOutItem']['item']['description'], "mobile")
        self.assertEqual(test_item_['updateMerchandiseTransferOutItem']['merchandiseTransferOutItem']['quantity'], 5)
        self.assertEqual(test_item_['updateMerchandiseTransferOutItem']['merchandiseTransferOutItem']['merchandiseTransferOut']['approvedBy']['username'], "user1")




class TestDeleteMerchandiseTransferOutItem(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                
                user1: createUser(email:"user@example.com" password:"password" username:"user1"){
                                user{
                            id,
                            username,
                            email,
                            password,    
                            }    
                        }
                user2: createUser(email:"user2@example.com" password:"password" username:"user2"){
                        user{
                    id,
                    username,
                    email,
                    password,    
                    }    
                }

                createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }

            createSupplier(input:{firstName:"supplier_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1222,store:1,supplier:1,image:"not_avial"}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        cls.us=user.objects.get(id=2)
        cls.executed = execute_test_client_api_query(
        
            """
           mutation{
                createMerchandiseTransferOut(input:{approvedBy:1,status:"approved",store:1}){
                    merchandiseTransferOut{
                        status,
                        store{
                            name
                        },
                        requestedBy{
                            username
                        },
                        approvedBy{
                            username,
                        }
                    }
                }
                createMerchandiseTransferOutItem(input:{item:1,quantity:3,merchandiseTransferOut:1}){
                    merchandiseTransferOutItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferOut{
                        approvedBy {
                        username
                        },
                        requestedBy {
                        username
                        },
                    }
                    }
                }
            
            }
            """
        , cls.us)
        # print("-->",cls.executed.get('data'))
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        us=user.objects.get(id=2)
        executed = execute_test_client_api_query(
        
            """
           mutation{
                deleteMerchandiseTransferOutItem(input:{id:1}){
                    merchandiseTransferOutItem{
                    item{
                        name,
                        description,
                    }
                    quantity,
                    merchandiseTransferOut{
                        approvedBy {
                        username
                        },
                        requestedBy {
                        username
                        },
                    }
                    }
                }
                
            }
            
            
            """
        , us)
        test_item_ = executed.get('data')
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['deleteMerchandiseTransferOutItem']['merchandiseTransferOutItem']['item']['name'], "Phone")
        self.assertEqual(test_item_['deleteMerchandiseTransferOutItem']['merchandiseTransferOutItem']['item']['description'], "mobile")
        self.assertEqual(test_item_['deleteMerchandiseTransferOutItem']['merchandiseTransferOutItem']['quantity'], 3)
        self.assertEqual(test_item_['deleteMerchandiseTransferOutItem']['merchandiseTransferOutItem']['merchandiseTransferOut']['approvedBy']['username'], "user1")





class TestCreateWastage(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.schema = core_schema.schema
        cls.test_item=cls.schema.execute(
            """
           mutation{
                createStore(input:{name:"store2"}){
                    store{
                        name,
                    }
                }
                

                createItemCategory(input:{name:"electronics"}){
                itemCategory{
                    name,
                }
                }

            createSupplier(input:{firstName:"supplier_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
                supplier{
                id,
                firstName,
                lastName,
                phoneNumber,
                email,
                address,
                }
            }
            createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1222,store:1,supplier:1,image:"not_avial"}){
                    item{
                        name,
                        description,
                        category{
                        name,
                        },
                        price,
                        store{
                        name,
                        },
                        supplier{
                        firstName
                        },
                        image,
                    }
                }
            }
            """
        )
        
        
        

    
    def test_mutate_and_get_payload(self):
        # log=self.c.login(username="user2",password="password")
        # print(">>",log,"<<")

        # test_item_=self.schema.execute(
        
        test_item_=self.schema.execute(
        
            """
           mutation{
                createWastage(input:{item:1,quantity:2,date:"2006-01-02T15:04:05"}){
                    wastage{
                    date,
                    quantity,
                    item{
                        name
                    }
                    }
                }
                
            }
            
            
            """
        )
        test_item_ = test_item_.data
        # print(">>>>",test_item_)
        self.assertEqual(test_item_['createWastage']['wastage']['date'], "2006-01-02T15:04:05")
        self.assertEqual(test_item_['createWastage']['wastage']['quantity'], 2)
        self.assertEqual(test_item_['createWastage']['wastage']['item']['name'], "Phone")




# class TestUpdateWastage(TestCase):
#     @classmethod
#     def setUpTestData(cls):

#         cls.schema = core_schema.schema
#         cls.test_item=cls.schema.execute(
#             """
#            mutation{
#                 createStore(input:{name:"store2"}){
#                     store{
#                         name,
#                     }
#                 }
                

#                 createItemCategory(input:{name:"electronics"}){
#                 itemCategory{
#                     name,
#                 }
#                 }

#             createSupplier(input:{firstName:"supplier_first_name",lastName:"y",phoneNumber:"0913129381",email:"x@y.com",address:"ayertena"}){
#                 supplier{
#                 id,
#                 firstName,
#                 lastName,
#                 phoneNumber,
#                 email,
#                 address,
#                 }
#             }
#             createItem(input:{name:"Phone",description:"mobile",itemCategory:1,price:1222,store:1,supplier:1,image:"not_avial"}){
#                     item{
#                         name,
#                         description,
#                         category{
#                         name,
#                         },
#                         price,
#                         store{
#                         name,
#                         },
#                         supplier{
#                         firstName
#                         },
#                         image,
#                     }
#                 }
#             createWastage(input:{item:1,quantity:2,date:"2006-01-02T15:04:05"}){
#                     wastage{
#                     date,
#                     quantity,
#                     item{
#                         name
#                     }
#                     }
#                 }
#             }
#             """
#         )
        
        
        

    
#     def test_mutate_and_get_payload(self):
#         # log=self.c.login(username="user2",password="password")
#         # print(">>",log,"<<")

#         # test_item_=self.schema.execute(
        
#         test_item_=self.schema.execute(
        
#             """
#            mutation{
#                 updateWastage(input:{id:1,item:1,quantity:5,date:"2007-01-02T15:04:05"}){
#                     wastage{
#                     date,
#                     quantity,
#                     item{
#                         name
#                     }
#                     }
#                 }
                
#             }
            
            
#             """
#         )
#         test_item_ = test_item_.data
#         print(">>>>",test_item_)
#         self.assertEqual(test_item_['updateWastage']['wastage']['date'], "2006-01-02T15:04:05")
#         self.assertEqual(test_item_['updateWastage']['wastage']['quantity'], 2)
#         self.assertEqual(test_item_['updateWastage']['wastage']['item']['name'], "Phone")



