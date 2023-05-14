from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PlaygroundFrom
from analizer.analizer import analize_text

@login_required(login_url='/login/')  
def playground_view(request):
    context = {
        'results': [0,0,0]
    }
    if request.method == 'POST':
        form = PlaygroundFrom(request.POST)
        if form.is_valid():
            textToAnalize = request.POST['text']
            results = analize_text(textToAnalize)
            results = [round(i * 100,1) for i in results]
            context['results']=results
    else:
        form = PlaygroundFrom()
    

    context['form']=form

    return render(request, 'playground/playground.html', context)
