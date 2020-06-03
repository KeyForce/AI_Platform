import os

from django.shortcuts import HttpResponse
from django.shortcuts import render

from CNN_Visual.visual_all_feature import *
from Platform.models import *
from .utils import get_file_list


# Create your views here.
def home(request):
    if request.method == 'POST':
        img = ImageInfo(img=request.FILES.get('img'))
        img.save()
        # show_img = ImageInfo.objects.all()
        model = MyNet()

        Transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor(),
            transforms.Normalize([0.49139968, 0.48215827, 0.44653124],
                                 [0.24703233, 0.24348505, 0.26158768])
        ])

        # heatmap_name = os.listdir('J:/Main Project/AI_Platform/image/heatmap')
        heatmap_name = get_file_list('J:/Main Project/AI_Platform/image/heatmap')
        heatmap = []
        for i in heatmap_name:
            heatmap.append({'name': i,
                            'url': '/image/heatmap/' + i})

        return render(request, 'home.html', {'img': img, 'heatmap': heatmap})
    else:
        return render(request, 'home.html', {})


def geek(request):
    import requests
    import json
    try:
        api_requets = requests.get('http://api.github.com/users?since=0')
        api = json.loads(api_requets.content)
        api_requets.close()
    except requests.exceptions.ConnectionError as e:
        print("连接超时")
        print(e)
        api = None

    return render(request, 'geek.html', {'api': api})


def user(request):
    if request.method == 'POST' and request.POST['user']:
        user = request.POST['user']
        import requests
        import json
        api_requets = requests.get('https://api.github.com/users/' + user)
        username = json.loads(api_requets.content)
        api_requets.close()
        return render(request, 'user.html', {'user': user, 'username': username})
    else:
        notfound = '请在搜索框输入你要搜索的内容...'
        return render(request, 'user.html', {'notfound': notfound})


def db_handle(request):
    models.UserInfo.objects.create(username='andy', password='123456', age=33)
    return HttpResponse('OK')


def upload_img(request):
    if request.method == 'POST':
        img = ImageInfo(img=request.FILES.get('img'))
        img.save()
    return render(request, 'home.html', {'img': img})

