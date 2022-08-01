from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType



admin_permissions=[
    'Can add log entry', 
    'Can view log entry',
    'Can add group',
    'Can change group',
    'Can delete group',
    'Can view group',
    'Can delete user',
    'Can view user'
]



store_managers_permissions=[
    'Can add item',
    'Can change item',
    'Can delete item',
    'Can view item',
    'Can add store',
    'Can view store',
    'Can delete store',
    'Can change store',
    'Can add item_category',
    'Can change item_category',
    'Can delete item_category',
    'Can view item_category',
    'Can add merchandise_transfer_in',
    'Can change merchandise_transfer_in',
    'Can delete merchandise_transfer_in',
    'Can view merchandise_transfer_in',
]
general_managers_permission=[
    'Can View log entry',
    'Can view supplier',
]
store_staff_permission=[
    'Can add item',
    'Can change item',
    'Can delete item',
    'Can view item',
    'Can view item_category',
    'Can add merchandiseTransferItem',
    'Can view merchandiseTransferItem',
    'Can delete merchandiseTransferItem',
    'Can change merchandiseTransferItem',
    'Can view repair_request',
    'Can change repair_request',
    'Can delete repair_request',
    'Can add wastage',
    'Can view wastage',
    'Can delete wastage',
    'Can change wastage',
]
employyes_permissions=[
    'Can add repair_request',
    'Can delete repair_request',
]

purchasers_permissions=[
    'Can add supplier',
    'Can view supplier',
    'Can change supplier',
    'Can delete supplier',
]

finance_permissions=[
    'Can add supplier',
    'Can view supplier',
    'Can change supplier',
    'Can delete supplier',
]





# def set_permissions():
    

def create_group():
    admins, created = Group.objects.get_or_create(name ='Admins')
    store_managers, created = Group.objects.get_or_create(name ='Store Manager')
    general_managers, created = Group.objects.get_or_create(name ='General Manager')
    store_staff, created = Group.objects.get_or_create(name ='Store Staff')
    employees, created = Group.objects.get_or_create(name ='Employees')
    purchasers, created = Group.objects.get_or_create(name ='Purchasers')
    finance, created = Group.objects.get_or_create(name ='Finance')
    for permission in admin_permissions:
        admins.permissions.add(Permission.objects.get(name=permission))
    for permission in store_managers_permissions:
        store_managers.permissions.add(Permission.objects.get(name=permission))
    for permission in store_managers_permissions:
        general_managers.permissions.add(Permission.objects.get(name=permission))
    for permission in store_staff_permission:
        store_staff.permissions.add(Permission.objects.get(name=permission))
    for permission in employyes_permissions:
        employees.permissions.add(Permission.objects.get(name=permission))
    for permission in purchasers_permissions:
        purchasers.permissions.add(Permission.objects.get(name=permission))
    for permission in finance_permissions:
        finance.permissions.add(Permission.objects.get(name=permission))