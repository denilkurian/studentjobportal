from django.contrib import admin
from .models import profile,Jobs,Notifications,Review,Company


admin.site.register(profile)
admin.site.register(Jobs)
admin.site.register(Review)
admin.site.register(Notifications)
admin.site.register(Company)