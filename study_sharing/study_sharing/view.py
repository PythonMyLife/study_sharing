# -*- coding: utf-8 -*-
import os
import re
import sys
import os.path 
import chardet
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import StreamingHttpResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

data_list = []
global data_list
'''data_list = os.listdir("static\\")
data1 = []
print data_list
for data in data_list:
    data_new = data.decode('gbk').decode('utf-8')
    data1 += [data_new]
data_list = data1
print data_list'''



reload(sys)
sys.setdefaultencoding('utf-8')


def fuzzyfinder(user_input, collection):
        suggestions = []
        pattern = '.*'.join(user_input) # Converts 'djm' to 'd.*j.*m'
        regex = re.compile(pattern)     # Compiles a regex.
        for item in collection:
            match = regex.search(item)  # Checks if the current item matches the regex.
            if match:
                suggestions.append((len(match.group()), match.start(), item))
        return [x for _, _, x in sorted(suggestions)]


def page1(request):
    request.session['account'] = 'nopeople'
    return render_to_response('hello.html')

@csrf_exempt
def download(request):
    global data_list
    if request.GET:
        content = request.GET.get('do-search',' ')
        data_s = fuzzyfinder(content, data_list)
        return render(request,'page-download.html',{'data_list' : data_s})
    if request.POST:
        for data in data_list:
            if request.POST.has_key(data):
                filepath = 'static\\' + data;
                file = open(filepath,'rb')  
                response = FileResponse(file)  
                response['Content-Type']='application/octet-stream'  
                response['Content-Disposition']='attachment;filename="{0}"'.format(data.encode('utf-8')) 
                return response
    global data_list
    data_list = os.listdir("static\\")
    data1 = []
    for data in data_list:
        data_new = data.decode(encoding='gbk').decode(encoding='utf-8')
        data1 += [data_new]
    data_list = data1
    data_list = data1
    return render(request,'page-download.html',{'data_list':data_list})

@csrf_exempt
def upload(request):
    if request.method == "POST":    
        myFile =request.FILES.get("myfile", None)   
        if not myFile:
            message = "请选择要上传的文件!"
            return render(request,"page-upload.html",{"message" : message})
        extention = os.path.splitext(myFile.name)[1]
        if request.POST['name'] == '':
            message = "文件名不能为空!"
            return render(request,"page-upload.html",{"message" : message})
        name = request.POST['name'] + extention
        if name in data_list:
            message = "文件名重复，请更换文件名!"
            return render(request,"page-upload.html",{"message" : message})
        destination = open(os.path.join("static\\",name),'wb+')
        #destination = open(os.path.join("static\\",myFile.name),'wb+')   
        for chunk in myFile.chunks():      
            destination.write(chunk)
        destination.close()
        global data_list
        #data_list += [myFile.name]
        data_list += [name]
        message = "上传成功！"
        return render(request,"page-upload.html",{"message" : message})
    else:
        return render_to_response('page-upload.html',{"message" : ""})

@csrf_exempt
def login(request):
    if request.method == "POST":
        if request.POST['account_name'] == 'keeper'and request.POST['pass_word'] == 'pass0of0keeper':
                request.session['account'] = 'keeper'
                return HttpResponseRedirect("/page-keep")
        request.session['account'] = 'nopeople'
        message = "用户名或密码错误！"
        return render(request,"page-login.html",{"message" : message})
    else:
        return render_to_response('page-login.html')


#@login_required
def keep(request):
    request.session.setdefault('account','nopeople')
    if request.session['account'] != 'keeper':
        return HttpResponseRedirect("/page-login")
    global data_list
    if request.POST:
        for data in data_list:
            if request.POST.has_key(data):
                filepath = 'static\\' + data;
                if(os.path.exists(filepath)):
                    os.remove(filepath)
                    data_list.remove(data)
                    return render_to_response('page-keep.html',{'data_list':data_list})
                else:
                    return HttpResponse("删除失败！")
    global data_list
    data_list = os.listdir("static\\")
    data1 = []
    for data in data_list:
        data_new = data.decode(encoding='gbk').decode(encoding='utf-8')
        data1 += [data_new]
    data_list = data1
    return render(request,'page-keep.html',{'data_list':data_list})

@csrf_exempt
def search(request):
    content = request.GET.get('do-search')
    global data_list
    data_s = []
    for data in data_list:
        if content in data:
            data_s += [content]
    return render(request, page-download.html,{data_list : data_s})
