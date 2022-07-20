from .models import *
from django.contrib import admin
# Register your models here.

admin.site.register(item)
admin.site.register(item_category)
admin.site.register(supplier)
admin.site.register(store)
admin.site.register(merchandise_transfer_in)
admin.site.register(merchandise_transfer_out)
admin.site.register(repair_request)
admin.site.register(wastage)

