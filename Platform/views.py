from django.shortcuts import render


# Create your views here.
def home(request):
    import requests
    import json
    try:
        api_requets = requests.get('http://api.github.com/users?since=0')
        api = json.loads(api_requets.content)
    except requests.exceptions.ConnectionError as e:
        print("连接超时")
        print(e)
        api = None

    return render(request, 'home.html', {'api': api})


def user(request):
    print(request)
    if request.method == 'POST':
        user = request.POST['user']
        import requests
        import json
        api_requets = requests.get('https://api.github.com/users/' + user)
        username = json.loads(api_requets.content)
        return render(request, 'user.html', {'user': user, 'username': username})
    elif request.method == 'GET':
        notfound = '请在搜索框输入你要搜索的内容...'
        return render(request, 'user.html', {'notfound': notfound})
    else:
        notfound = '请在搜索框输入你要搜索的内容...'
        return render(request, 'user.html', {'notfound': notfound})
