from django.shortcuts import render


# Create your views here.
def home(request):
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

    return render(request, 'home.html', {'api': api})


def user(request):
    if request.method == 'POST' and request.POST['user']:
        user = request.POST['user']
        import requests
        import json
        api_requets = requests.get('https://api.github.com/users/' + user)
        api_requets.close()
        username = json.loads(api_requets.content)
        return render(request, 'user.html', {'user': user, 'username': username})
    else:
        notfound = '请在搜索框输入你要搜索的内容...'
        return render(request, 'user.html', {'notfound': notfound})
