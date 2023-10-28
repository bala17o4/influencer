from django.contrib import admin
from .models import User, AppliedBy, Ad

# Register your models here.
admin.site.register(User)
admin.site.register(AppliedBy)
admin.site.register(Ad)