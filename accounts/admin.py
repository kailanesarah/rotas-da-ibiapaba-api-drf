from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import Category, Location, User, Establishment
from app.utils import RelatedFieldExtractorAdmin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'state', 'city', 'CEP', 'neighborhood', 'street', 'number')
    search_fields = ('city', 'state', 'country')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'type', 'is_staff', 'is_active')
    list_filter = ('type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'type')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'type', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):

    def get_category(self, obj):
        extractor = RelatedFieldExtractorAdmin() 
        return extractor.get_field(obj, 'category') 

    list_display = ('id', 'name', 'CNPJ', 'email', 'whatsapp', 'user', 'location', 'get_category')
    search_fields = ('name', 'email', 'CNPJ')
    list_filter = ('user__type',)




