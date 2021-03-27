from django.contrib import admin

# Register your models here.

from .models import Location, Book, User, Money, BookDonate, Stationery, StationeryDonate, Manager

admin.site.register(Location)
admin.site.register(Book)
admin.site.register(User)
admin.site.register(Money)
admin.site.register(BookDonate)
admin.site.register(Stationery)
admin.site.register(StationeryDonate)
admin.site.register(Manager)

