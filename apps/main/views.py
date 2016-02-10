# -*- coding: utf-8 -*- 

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.template import Context
from django.core.mail import send_mail
from django.template.loader import get_template

from main.models import *
from main.forms import *

####################################################################################################
## stuff
####################################################################################################

def toInt(*args):
    result = []
    for x in args:
        if x:
            result.append(int(x))
        else:
            result.append(0)
    return result

def splitPhone(phone):
    if ')' in phone:
        code, phone = phone.split(')', 1)
        code += ')'
    else:
        code = ''
    return code.strip(), phone.strip()
    
def renderToResponse(request, template, vars, mimetype=None):
    for k, v in getVars().items():
        vars[k] = v
        
    vars['mainMenu'] = Page.objects.filter(is_menu=True)
    vars['phoneCode'], vars['phone'] = splitPhone(vars['phone'])

    if mimetype:
        return render_to_response(template, vars, mimetype=mimetype)
    else:
        return render_to_response(template, vars)


def emailTemplate(emailFrom, emailTo, tmplFile, vars):
    emailFrom = 'aaa@gmail.com'
    t = get_template(tmplFile)
    s = t.render(Context(vars))
    subject, body = s.split('\n', 1)
    subject = subject.strip()
    body = body.strip()
    # send_mail(subject, body, emailFrom, [emailTo], fail_silently=False)
    i = Incoming(title=subject, content=body)
    i.save()
    return 'mail "%s" => "%s"\n%s\n%s\n%s' % (emailFrom, emailTo, subject, '-'*30, body)
    
####################################################################################################
## pages
####################################################################################################

def index(request):
    page = getPage('index')
    # .order_by('?')
    faq = Faq.objects.all()[:1]
    events = Event.objects.all()[:2]
    products = Product.objects.all()[:2]
    facts = Fact.objects.all()[:2]
    return renderToResponse(request, 'index.html', locals())
    
def page(request, slug, subSlug=None):
    page = get_object_or_404(Page, slug=slug)
    if subSlug:
        page = get_object_or_404(SubPage, slug=subSlug)
        slug2 = '%s/%s' % (slug, subSlug)
    return renderToResponse(request, 'page.html', locals())

def colNoGenerator(colCount):
    ''' генерит последовательность 0 1 2 3 4 4 3 2 1 0 0 1 2 3 4 4 3 2 1 0 0 1 2 3... '''
    colNoList = list(range(colCount))+list(range(colCount-1, -1, -1))
    i = 0
    while 1:
        yield colNoList[i]
        i += 1
        if i == len(colNoList):
            i = 0

def buy(request):
    page = getPage('buy')
    
    def cmp(country1, country2):
        return country2.addressCount()-country1.addressCount()
        
    countryList = [i for i in Country.objects.all() if i.addressCount()]
    countryList = sorted(countryList, cmp)
        
    colCount = var('buyColCount')
    colList = [[] for i in range(colCount)]
    colNoGen = colNoGenerator(colCount)
    for country in countryList:
        i = colNoGen.next()
        colList[i].append(country)
    colList = [col for col in colList if col]
        
    return renderToResponse(request, 'buy.html', locals())

def faq(request):
    page = getPage('faq')
    items = Faq.objects.all()
    
    if request.method == 'POST':
        form = FaqForm(request.POST)
        if form.is_valid():
            vars = form.cleaned_data
            emailDump = emailTemplate(var('emailFaq'), var('emailFaq'), 'faq.txt', vars)
            form = FaqForm()
    else:
        form = FaqForm()
        
    return renderToResponse(request, 'faq.html', locals())
    
def events(request, id=None):
    page = getPage('events')
    if id:
        id = int(id)
        event = get_object_or_404(Event, id=id)
        return renderToResponse(request, 'event-item.html', locals())
    else:
        items = Event.objects.all()
        return renderToResponse(request, 'events.html', locals())
    
def facts(request, id=None):
    page = getPage('facts')
    items = Fact.objects.all()
    if id:
        id = int(id)
        fact = get_object_or_404(Fact, id=id)
        return renderToResponse(request, 'fact-item.html', locals())
    else:
        return renderToResponse(request, 'facts.html', locals())
    
def products(request, id=None):
    page = getPage('products')
    if id:
        id = int(id)
        product = get_object_or_404(Product, id=id)
        return renderToResponse(request, 'product-item.html', locals())
    else:
        items = Product.objects.all()
        return renderToResponse(request, 'products.html', locals())
    
def contact(request):
    page = getPage('contact')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            vars = form.cleaned_data
            emailDump = emailTemplate(var('emailContact'), var('emailContact'), 'contact.txt', vars)
            form = ContactForm()
    else:
        form = ContactForm()
        
    return renderToResponse(request, 'contact.html', locals())
    
def _404(request):
    return render_to_response('404.html', locals())