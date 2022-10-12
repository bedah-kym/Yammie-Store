from django.contrib import admin
from .models import profile,PromoCode

class PromoInline(admin.TabularInline):
    model=PromoCode

class ProfileAdmin(admin.ModelAdmin):
    fieldsets=[
    (' ',{"fields":['user_name']}),
    ('agent details ',{"fields":['is_anon_agent','is_sales_agent','cell_number','commission']}),
    ]
    inlines=[PromoInline]
    list_display=['user_name','is_anon_agent','is_sales_agent','cell_number']
    list_filter = ['is_anon_agent','is_sales_agent']

admin.site.register(profile,ProfileAdmin)
#admin.site.register(PromoCode)
