import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from authentication.models import user
from .models import *

class customerFilter(django_filters.FilterSet):
    class Meta:
        model = customer
        fields = ['first_name', 'last_name']

class customerNode(DjangoObjectType):
    class Meta:
        model = customer
        interfaces = (graphene.relay.Node,)

class salesOrderFilter(django_filters.FilterSet):
    class Meta:
        model = salesOrder
        fields = ['item', 'customer']

class salesNode(DjangoObjectType):
    class Meta:
        model = salesOrder
        interfaces = (graphene.relay.Node,)

class invoiceFilter(django_filters.FilterSet):
    class Meta:
        model = invoice
        fields = ['sales_order']

class invoiceNode(DjangoObjectType):
    class Meta:
        model = invoice
        interfaces = (graphene.relay.Node,)

"""CRUD for sales"""

class createSalesOrder(graphene.relay.ClientIDMutation):
    sale = graphene.Field(salesNode)

    class Input:
        item = graphene.ID()
        customer = graphene.ID()
        quantity = graphene.Int()

    def mutate_and_get_payload(self, info, **input):
        sales_person = info.context.user
         # sales_person=user.objects.filter(id=user.id)

        Item = item.objects.get(id=input.get('item'))
        Customer = customer.objects.get(id=input.get('customer'))
        sale = salesOrder(item=Item, customer=Customer, quantity=input.get('quantity'), sales_person=sales_person)
        sale.save()

        return createSalesOrder(sale=sale)

class updateSalesOrder(graphene.Mutation):
    sale = graphene.Field(salesNode)

    class Input:
        id = graphene.ID()
        item = graphene.ID()
        customer = graphene.ID()
        quantity = graphene.Int()
        sales_person = graphene.ID()

    def mutate(self, info, **input):
        sale = salesOrder.objects.get(id=id)
        sale.item = item.objects.get(id=input.get('item'))
        sale.customer = customer.objects.get(id=input.get('customer'))
        sale.quantity = input.get('quantity')

        sale.save()
        return updateSalesOrder(sale=sale)

class deleteSalesOrder(graphene.relay.ClientIDMutation):

    sale = graphene.Field(salesNode)
    
    class Input:
        id = graphene.Int()

    def mutate_and_get_payload(self, info, id):
        sale = salesOrder.objects.get(id=id)
        sale.delete()
        return deleteSalesOrder(sale=sale)


"""CRUD for customers"""

class createCustomers(graphene.relay.ClientIDMutation):
    customer = graphene.Field(customerNode)

    class Input:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        address = graphene.String()

    def mutate_and_get_payload(root,info ,**input):
        created_customer = customer(first_name=input.get('first_name'), last_name=input.get('last_name'), email=input.get('email'), phone_number=input.get('phone'), address=input.get('address'))
        created_customer.save()
        return createCustomers(customer=created_customer)

class updateCustomer(graphene.relay.ClientIDMutation):

    customer = graphene.Field(customerNode)

    class Input:
        id = graphene.Int()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        address = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        customer = customer.objects.get(id=input.get('id'))
        customer.first_name = input.get('first_name')
        customer.last_name = input.get('last_name')
        customer.email = input.get('email')
        customer.phone_number = input.get('phone')
        customer.address = input.get('address')
        customer.save()
        return updateCustomer(customer=customer)

class deleteCustomer(graphene.relay.ClientIDMutation):
    customer = graphene.Field(customerNode)

    class Input:
        id = graphene.Int()

    
    def mutate_and_get_payload(root, info, id):
        customer = customer.objects.get(id=id)
        customer.delete()
        return deleteCustomer(customer=customer)

"""CRUD for invoices"""

class createInvoice(graphene.relay.ClientIDMutation):
    invoice = graphene.Field(invoiceNode)
    class Input:
        sales_order = graphene.Int()
        paid_amount = graphene.Float()

    def mutate_and_get_payload(self, info, **input):
        sales_person = info.context.user
        sales_order = salesOrder.objects.get(id=input.get('sales_order'))
        Invoice = invoice(sales_order=sales_order, paid_amount=input.get('paid_amount'), sales_person=sales_person)
        
        Invoice.save()
        return createInvoice(invoice=Invoice)

class updateInvoice(graphene.relay.ClientIDMutation):
    invoice = graphene.Field(invoiceNode)
    class Input:
        id = graphene.Int()
        sales_order = graphene.ID()
        # invoice_number = graphene.String()
        # invoice_date = graphene.String()
        paid_amount = graphene.Float()
        # due_date = graphene.String()

    def mutate_and_get_payload(self, info, **input):
        invoice = invoice.objects.get(id=input.get('id'))
        invoice.sales_order = input.get('sales_order')
        invoice.paid_amount = input.get('paid_amount')

        invoice.save()
        return updateInvoice(invoice=invoice)

class deleteInvoice(graphene.relay.ClientIDMutation):
    invoice = graphene.Field(invoiceNode)

    class Input:
        id = graphene.Int()

    def mutate_and_get_payload(self, info, id):
        invoice = invoice.objects.get(id=id)
        invoice.delete()
        return deleteInvoice(invoice=invoice)

class mutation(graphene.ObjectType):
    create_sales = createSalesOrder.Field()
    update_sales = updateSalesOrder.Field()
    delete_sales = deleteSalesOrder.Field()

    create_customer = createCustomers.Field()
    update_customer = updateCustomer.Field()
    delete_customer = deleteCustomer.Field()
    
    create_invoice = createInvoice.Field()
    update_invoice = updateInvoice.Field()
    delete_invoice = deleteInvoice.Field()

#Queries

class query(graphene.ObjectType):
    sales=graphene.relay.Node.Field(salesNode)
    customer=graphene.relay.Node.Field(customerNode)
    invoice=graphene.relay.Node.Field(invoiceNode)
    all_sales=relay_items = DjangoFilterConnectionField(salesNode, filterset_class=salesOrderFilter)
    all_customers=relay_items = DjangoFilterConnectionField(customerNode, filterset_class=customerFilter)
    all_invoices=relay_items = DjangoFilterConnectionField(invoiceNode, filterset_class=invoiceFilter)


class schema(graphene.Schema):
    query = query
    mutation = mutation