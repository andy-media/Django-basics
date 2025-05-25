from django.contrib import admin
from .models import School, Contestant, Coach, Payment, Document, User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from unfold.admin import StackedInline, TabularInline

from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin



class ContestantInline(TabularInline):
    model = Contestant
    extra = 0

class CoachInline(TabularInline):
    model = Coach
    extra = 0

class PaymentInline(TabularInline):
    model = Payment
    extra = 0

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_school_admin')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_school_admin')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_school_admin', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_school_admin'),
        }),
    )
 


@admin.register(School)
class SchoolAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    # export_form_class = SelectableFieldsExportForm
    list_display = ('name_of_school','region', 'location', 'registration_complete', 'payment_verified')
    list_filter = ('registration_complete', 'payment_verified', 'region')
    search_fields = ('name_of_school','region', 'location')
    list_filter_submit = True 
    inlines = [ContestantInline, CoachInline, PaymentInline]

@admin.register(Payment)
class PaymentAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    export_form_class = SelectableFieldsExportForm
    list_display = ('school', 'amount', 'verified', 'date_created')
    # list_filter = ('verified', 'date_created')
    search_fields = ('school__name_of_school', 'paystack_ref')
    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = (
        
        ("date_created", RangeDateFilter),  # Date filter
        
    )

@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    list_display = ('title', 'uploaded',)