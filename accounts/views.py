from django.shortcuts import render
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        pass
    else:
        form = CustomUserCreationForm()

    context = {
            'form': form,
    }
    return render(request, 'signup.html', context)