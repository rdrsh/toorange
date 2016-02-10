# -*- coding: utf-8 -*- 

from types import *

from django.db import models
from settings import DEFAULT_VARS

####################################################################################################
## Vars
####################################################################################################

class Var(models.Model):
    name = models.SlugField(max_length=255, verbose_name=u'Название', unique=True)
    value = models.CharField(max_length=255, verbose_name=u'Значение')
    comment = models.CharField(max_length=255, verbose_name=u'Коментарий')
    
    def __unicode__(self):
        return u'%s = %s' % (self.comment, self.value)
        
    class Meta:
        verbose_name = u"Настройки"
        verbose_name_plural = u"Настройки"
        ordering = ('name',)

####################################################################################################
## getVars
####################################################################################################

def isInt(x):
    return type(x) is IntType

def getVars():
    vars = {}
    dbVars = dict([i.name, i.value] for i in Var.objects.all())
    for k, v in DEFAULT_VARS.items():
        if k in dbVars:
            if isInt(v):
                v = int(dbVars[k])
            else:
                v = dbVars[k]
        vars[k] = v
    return vars
    
def var(name):
    VARS = getVars()
    return VARS[name]

####################################################################################################
## page
####################################################################################################

class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    slug = models.SlugField(max_length=255, verbose_name=u'URL', unique=True)
    content = models.TextField(verbose_name=u'Содержание', blank=True)
    sort_no = models.FloatField(verbose_name=u'Порядковый номер', blank=True, default=100)
    is_menu = models.BooleanField(verbose_name=u'В главном меню', default=False)

    childCache = None
    def subPageList(self):
        if not self.childCache:
            self.childCache = SubPage.objects.filter(page=self)
        return self.childCache
        
    def level2(self):
        return self.subPageList()

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"Раздел"
        verbose_name_plural = u"Разделы"
        ordering = ('sort_no',)
        
def getPage(slug):
    try:
        p = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        t = 'Раздел "%s" не заполнен' % slug
        c = '<h1>Ошибка</h1><p>%s</p><br/>' % t
        p = Page(slug=slug, title=t, content=c)
        p.save()
        c += '<a href="/admin/main/page/%d/" target="_blank">заполнить</a><hr style="margin-bottom:100px;"/>' % p.id
        p.content = c
        p.save()
    return p

class SubPage(models.Model):
    page = models.ForeignKey(Page, verbose_name=u'Раздел')
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    slug = models.SlugField(max_length=255, verbose_name=u'URL', unique=True)
    content = models.TextField(verbose_name=u'Содержание', blank=True)
    sort_no = models.FloatField(verbose_name=u'Порядковый номер', blank=True, default=100)

    def level2(self):
        return self.page.level2()

    def slug2(self):
        return '%s/%s' % (self.page.slug, self.slug)

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"Страница"
        verbose_name_plural = u"Страницы"
        ordering = ('sort_no',)
        
####################################################################################################
## 
####################################################################################################

class Faq(models.Model):
    question = models.TextField(verbose_name=u'Вопрос')
    answer = models.TextField(verbose_name=u'Ответ')
    sort_no = models.FloatField(verbose_name=u'Порядковый номер', blank=True, default=100)

    def __unicode__(self):
        return self.question
        
    class Meta:
        verbose_name = u"Вопрос-ответ"
        verbose_name_plural = u"Вопрос-ответ"
        ordering = ('sort_no',)

class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    annotation = models.TextField(verbose_name=u'Аннотация')
    content = models.TextField(verbose_name=u'Текст')
    created = models.DateField(auto_now=True, verbose_name=u'Дата')

    def __unicode__(self):
        return "%s. %s" % (self.created, self.title)
        
    class Meta:
        verbose_name = u"событие"
        verbose_name_plural = u"События"
        ordering = ('-created',)
        
class Fact(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    annotation = models.TextField(verbose_name=u'Аннотация')
    content = models.TextField(verbose_name=u'Текст')
    sort_no = models.FloatField(verbose_name=u'Порядковый номер', blank=True, default=100)

    def __unicode__(self):
        return self.title
        
    class Meta:
        verbose_name = u"Это интересно"
        verbose_name_plural = u"Это интересно"
        ordering = ('sort_no',)
        
w = 160
h = 160
class Product(models.Model):
    w = w
    h = h
    title = models.CharField(max_length=255, verbose_name=u'Название')
    img = models.ImageField(upload_to='img/product/', verbose_name=u'Изображение (%d X %d)' % (w, h))
    annotation = models.TextField(verbose_name=u'Анотация')
    description = models.TextField(verbose_name=u'Описание')
    sort_no = models.FloatField(verbose_name=u'Порядковый номер', blank=True, default=100)

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"Продукт"
        verbose_name_plural = u"Продукты"
        ordering = ('sort_no',)
        
class Img(models.Model):
    img = models.ImageField(upload_to='img/img/', verbose_name=u'Картинка')

    def __unicode__(self):
        return u'/%s' % self.img
    
    class Meta:
        verbose_name = u"Картинка"
        verbose_name_plural = u"Картинки"
        
class Incoming(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    content = models.TextField(verbose_name=u'Содержание')
    created = models.DateTimeField(auto_now=True, verbose_name=u'Дата')
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        verbose_name = u"Входящие"
        verbose_name_plural = u"Входящие"
        ordering = ('-created',)
        
####################################################################################################
## location
####################################################################################################

class Country(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Страна', unique=True)
    
    childCache = None
    def townList(self):
        if not self.childCache:
            self.childCache = Town.objects.filter(country=self)
        return self.childCache
    
    def townCount(self):
        return len(self.townList)
    
    def addressCount(self):
        return sum([t.addressCount() for t in self.townList()])
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        verbose_name = u"Страна продаж"
        verbose_name_plural = u"Страны продаж"
        ordering = ('title',)
        
class Town(models.Model):
    country = models.ForeignKey(Country, verbose_name=u'Страна')
    title = models.CharField(max_length=255, verbose_name=u'Город')
    
    childCache = None
    def addressList(self):
        if not self.childCache:
            self.childCache = Address.objects.filter(town=self)
        return self.childCache
        
    def addressCount(self):
        return len(self.addressList())
    
    def __unicode__(self):
        return u'%s/%s' % (self.country, self.title)
        
    class Meta:
        verbose_name = u"Город продаж"
        verbose_name_plural = u"Города продаж"
        ordering = ('title',)
        
class Address(models.Model):
    town = models.ForeignKey(Town, verbose_name=u'Город')
    title = models.CharField(max_length=255, verbose_name=u'Адрес')
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        verbose_name = u"Адрес продаж"
        verbose_name_plural = u"Адреса продаж"
        ordering = ('title',)
