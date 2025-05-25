from django.contrib import admin

from .models import Category, Blog, Comment, Author
# Register your models here.

from unfold.admin import StackedInline, TabularInline

from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Author)
class AuthorAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ('name', 'email')
    prepopulated_fields = {"slug": ("name",)}

class BlogAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    # export_form_class = SelectableFieldsExportForm
    prepopulated_fields = {
        'blog_slug': ('title',)
    }
    list_display = ('title','author',  'category', 'status', 'section', 'main_post')
    list_filter = ('status', 'category', 'main_post')
    search_fields = ('author','title', 'category')
    list_filter_submit = True 
    # inlines = [ContestantInline, CoachInline, PaymentInline]

class CategoryAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    prepopulated_fields = {
        'slug': ('name',)
    }

class CommentAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ('name', 'comment', 'date',)
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)