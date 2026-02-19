# core/admin.py
from django.contrib import admin
from django.contrib.admin import AdminSite

# Customize the admin site
admin.site.site_header = "CSHAMBA Farm Management"
admin.site.site_title = "CSHAMBA Admin Portal"
admin.site.index_title = "Welcome to CSHAMBA Farm Management System"