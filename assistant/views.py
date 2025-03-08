

from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchVector  
from .models import HistoricalEvent
from .utils import get_deepseek_response
from django.shortcuts import render
def index(request):
    context = {'response': None}
    
    if request.method == 'POST':
        user_input = request.POST.get('query', '').strip()
        
        # Поиск в базе данных
        search_results = HistoricalEvent.objects.filter(
            Q(title__icontains=user_input) |
            Q(description__icontains=user_input)
        )[:5]
        
        # Если нет результатов в БД - запрос к AI
        if not search_results:
            print(f"[DEBUG] Запрос к ИИ: {user_input}")
            try:
                ai_response = get_deepseek_response(user_input)
                print(f"[DEBUG] Ответ ИИ: {ai_response}")
                response = {
                    'type': 'ai',
                    'content': ai_response
                }
            except Exception as e:
                response = {
                    'type': 'error',
                    'content': f"Ошибка: {str(e)}"
                }
        else:
            response = {
                'type': 'db',
                'content': search_results
            }
        context['response'] = response
    return render(request, 'assistantstwo/index.html', context)
