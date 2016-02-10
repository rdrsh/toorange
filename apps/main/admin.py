# -*- coding: utf-8 -*-

from django.contrib import admin
from main.models import *

####################################################################################################
## vars
####################################################################################################    

class AdminCls(admin.ModelAdmin):
    class Meta:
        # dict полей для которых нужно установить соответствующий класс <input class="..."
        field_to_class = None
 
    # Добавляем класс wysiwyg для всех полей перечисленных в Meta.wysiwyg_fields
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(AdminCls, self).formfield_for_dbfield(db_field, **kwargs)
        if self.Meta.field_to_class:
            if db_field.name in self.Meta.field_to_class:
                field.widget.attrs['class'] = self.Meta.field_to_class[db_field.name] + ' ' + field.widget.attrs.get('class', '')
        return field

####################################################################################################
## vars
####################################################################################################    

class VarAdmin(admin.ModelAdmin):
    list_display = ('comment', 'value')
    list_editable = ('value',)
    
admin.site.register(Var, VarAdmin)

####################################################################################################
## pages
####################################################################################################    

class PageAdmin(AdminCls):
    class Meta:
        field_to_class = { 'content': 'editor' }
    list_display = ('title', 'slug', 'sort_no', 'is_menu',)
    list_editable = ('sort_no', 'is_menu',)
    search_fields = ('title', 'slug', 'content',)
    list_filter = ('is_menu',)
    
class SubPageAdmin(AdminCls):
    class Meta:
        field_to_class = { 'content': 'editor' }
    list_display = ('title', 'slug', 'sort_no',)
    list_editable = ('sort_no',)
    search_fields = ('title', 'slug', 'content',)
    list_filter = ('page',)
    
class ImgAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ('img',)
    
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'sort_no',)
    list_editable = ('sort_no',)
    search_fields = ('question', 'answer',)
    
class EventAdmin(AdminCls):
    class Meta:
        field_to_class = { 'content': 'editor', }    
    list_display = ('title', 'created')
    search_fields = ('title',)
    
class FactAdmin(AdminCls):
    class Meta:
        field_to_class = { 'content': 'editor', }    
    list_display = ('title', 'sort_no')
    list_editable = ('sort_no',)
    search_fields = ('title',)
    
class ProductAdmin(AdminCls):
    class Meta:
        field_to_class = { 'annotation': 'editor-sm', 'description': 'editor', }
    list_display = ('title', 'img', 'sort_no',)
    list_editable = ('sort_no',)
    search_fields = ('title', 'annotation', 'description',)
    
admin.site.register(Page, PageAdmin)
admin.site.register(SubPage, SubPageAdmin)
admin.site.register(Img, ImgAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Fact, FactAdmin)
admin.site.register(Product, ProductAdmin)

####################################################################################################
## incoming
####################################################################################################    

class IncomingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    
admin.site.register(Incoming, IncomingAdmin)

####################################################################################################
## incoming
####################################################################################################    

class CountryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
class TownAdmin(admin.ModelAdmin):
    list_display = ('title', 'country',)
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ('title', 'town',)
    
admin.site.register(Country, CountryAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(Address, AddressAdmin)
