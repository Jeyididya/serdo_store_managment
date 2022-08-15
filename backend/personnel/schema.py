import django_filters
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import employeeProfile
from authentication.models import user

class employeeProfileFilter(django_filters.FilterSet):
    class Meta:
        model = employeeProfile
        fields =['first_name', 'last_name']

class employeeProfileNode(DjangoObjectType):
    class Meta:
        model = employeeProfile
        interfaces = (graphene.relay.Node,)

class employeeProfileQuery(DjangoFilterConnectionField):
    employee_profile = graphene.relay.Node.Field(employeeProfileNode)
    all_employee_profiles = DjangoFilterConnectionField(employeeProfileNode, filterset_class=employeeProfileFilter)

"""Mutations for employeeProfile"""

class createEmployeeProfile(graphene.ClientIDMutation):
     employeeProfile=graphene.Field(employeeProfileNode)

     class Input:
            photo = graphene.String()
            first_name = graphene.String(required=True)
            last_name = graphene.String(required=True)
            role = graphene.String(required=True)
            cv = graphene.String(required=True)
            phone_number = graphene.String(required=True)
            address = graphene.String(required=True)
            user = graphene.ID(required=True)
            

     def mutate_and_get_payload(root, info, **input):
        user = user.objects.get(pk=input.get('user'))
        employee_profile = employeeProfile.objects.create(
            first_name=input.get('first_name'),
            last_name=input.get('last_name'),
            role=input.get('role'),
            cv=input.get('cv'),
            phone_number=input.get('phone_number'),
            address=input.get('address'),
            user=user,
            )
        return createEmployeeProfile(employee_profile=employee_profile)

class updateEmployeeProfile(graphene.ClientIDMutation):
    employeeProfile=graphene.Field(employeeProfileNode)

    class Input:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        role = graphene.String()
        cv = graphene.String()
        phone_number = graphene.String()
        address = graphene.String()
        user = graphene.ID()
        photo=graphene.String()

    def mutate_and_get_payload(root, info, **input):
        Employee_profile = employeeProfile.objects.get(pk=input.get('id'))
        Employee_profile.first_name = input.get('first_name')
        Employee_profile.last_name = input.get('last_name')
        Employee_profile.role = input.get('role')
        Employee_profile.cv = input.get('cv')
        Employee_profile.phone_number = input.get('phone_number')
        Employee_profile.address = input.get('address')
        Employee_profile.user = input.get('user')
        Employee_profile.photo = input.get('photo')
        Employee_profile.save()
        return updateEmployeeProfile(employee_profile=Employee_profile)

class deleteEmployeeProfile(graphene.ClientIDMutation):
    employeeProfile=graphene.Field(employeeProfileNode)

    class Input:
        id = graphene.ID(required=True)

    def mutate_and_get_payload(root, info, **input):
        employee_profile = employeeProfile.objects.get(pk=input.get('id'))
        employee_profile.delete()
        return deleteEmployeeProfile(employee_profile=employee_profile)

class employeeProfileMutation(graphene.ObjectType):
    create_employee_profile = createEmployeeProfile.Field()
    update_employee_profile = updateEmployeeProfile.Field()
    delete_employee_profile = deleteEmployeeProfile.Field()
