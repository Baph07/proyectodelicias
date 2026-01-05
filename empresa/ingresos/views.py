from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def ingresos(request):
    return render(request, 'ingresos/lista_ingresos.html')
