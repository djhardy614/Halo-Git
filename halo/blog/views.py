from django.shortcuts import render

post = [
    {
        'author': 'Dave',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'today',

    },
    {
        'author': 'Ruth',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'tomorrow',

    }
]


def home(request):
    context = {
        'posts': post
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title':'About'})
