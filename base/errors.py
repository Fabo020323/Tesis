from django.shortcuts import render


def error_400_view(request, exception):
    return render(request, 'pages-error.html',
                  {'status': 400, 'textini': '¡Vaya! Página no encontrada',
                   'text': 'Parece que has tomado un camino equivocado. No te preocupes... nos pasa a todos. Es posible que desees comprobar tu conexión a Internet.'},
                  status=400)


def error_403_view(request, exception):
    return render(request, 'pages-error.html', {'status': 403, 'textini': '¡Vaya! Sin permisos no te dejaremos Seguir',
                                                'text': 'Parece que has tomado un camino equivocado. No te preocupes... nos pasa a todos. Es posible que desees comprobar tu conexión a Internet.'},
                  status=403)


def error_404_view(request, exception):
    return render(request, 'pages-error.html', {'status': 404, 'textini': '¡Vaya! Página no encontrada',
                                                'text': 'Parece que has tomado un camino equivocado. No te preocupes... nos pasa a todos. Es posible que desees comprobar tu conexión a Internet.'},
                  status=404)


def error_405_view(request, exception):
    return render(request, 'pages-error.html', {'status': 405, 'textini': '¡Vaya! Método no permitido',
                                                'text': 'Parece que has tomado un camino equivocado. No te preocupes... nos pasa a todos. Es posible que desees comprobar tu conexión a Internet.'},
                  status=405)


def error_500_view(request):
    return render(request, 'pages-error.html', {'status': 500, 'textini': '¡Vaya! Tenemos un error en el Servidor',
                                                'text': 'Intenta más tarde actualizar la página.'}, status=500)
