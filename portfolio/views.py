from django.shortcuts import render

def home(request):
    context = {
        'name': 'Alex Morgan',
        'title': 'Full Stack Developer',
        'bio': 'I craft clean, scalable web experiences with a focus on performance and user delight.',
        'skills': ['Python', 'Django', 'JavaScript', 'React', 'Tailwind CSS', 'PostgreSQL'],
        'projects': [
            {
                'title': 'E-Commerce Platform',
                'desc': 'A full-featured online store with real-time inventory and payment integration.',
                'tags': ['Django', 'React', 'Stripe'],
                'link': '#',
            },
            {
                'title': 'Task Management App',
                'desc': 'Collaborative project tracker with live updates and team notifications.',
                'tags': ['Django', 'WebSockets', 'Tailwind'],
                'link': '#',
            },
            {
                'title': 'API Analytics Dashboard',
                'desc': 'Visual monitoring tool for REST APIs with custom alerting rules.',
                'tags': ['Python', 'D3.js', 'PostgreSQL'],
                'link': '#',
            },
        ],
    }
    return render(request, 'home.html', context)
