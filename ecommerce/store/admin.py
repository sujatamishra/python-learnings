from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
#admin.site.register(Product)
admin.site.register(ShippingAddress)


@admin.register(Product)
class Productadmin(ImportExportModelAdmin):
    list_display = ('name','price','digital','image')
