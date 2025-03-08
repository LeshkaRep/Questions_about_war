from openai import OpenAI
from django.conf import settings
from typing import Union

def validate_query(query: str) -> bool:
    required_keywords = [
        'война', 'татнефть', 'нефть', '1941', '1945', 'ссср', 
        'вов', 'история', 'битва', 'фронт', 'промышленность',
        'сталинград', 'ветераны', "ветеран" ,"события", "история", "дата", "даты" , "победа" , "солдаты" , "солдат" , "танк", "тыл", "враг","самолёты", "германия", "партизаны", "блокада" # Добавлено ключевое слово
    ]
    query_lower = query.lower()
    
    # Расширенная проверка для ВОВ
    if any(word in query_lower for word in ["великая отечественная", "великой отечественной", "сталинград"]):
        return True
    
    return any(kw in query_lower for kw in required_keywords)

def get_deepseek_response(prompt: str) -> Union[str, None]:
    if not validate_query(prompt):
        return "Запрос не соответствует тематике. Задайте вопрос о ВОВ или Татнефти. Проверьте написали ли вы без ошибки."
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

    system_message = """Ты исторический помощник. Формулируй ответы:
1. Для запросов о датах/событиях - краткий список фактов
2. Для аналитических вопросов - структурированный очерк с подзаголовками
3. Всегда упоминай источники информации (БД проекта или исторические документы)"""

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:8000",  
                "X-Title": "Historical Assistant",
            },
            model="openai/gpt-3.5-turbo-0613",
            messages=[
                {
                    "role": "system", 
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )
        response_content = completion.choices[0].message.content
        response_content = response_content.replace("\\boxed{", "").replace("}", "")
        return response_content if response_content.strip() else "Не удалось сгенерировать ответ."
    except Exception as e:
        print(f"[API ERROR] {str(e)}")  
        return f"Ошибка API: {str(e)}"