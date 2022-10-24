from django.contrib import admin
from .models import User, ResetCode

admin.site.register(User)
admin.site.register(ResetCode)
