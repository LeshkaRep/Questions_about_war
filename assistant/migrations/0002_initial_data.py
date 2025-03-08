from django.db import migrations

def add_initial_data(apps, schema_editor):
    HistoricalEvent = apps.get_model('assistant', 'HistoricalEvent')
    
    events = [
        {
            'title': 'Основание Татнефти',
            'description': 'ПАО «Татнефть» основано в 1950 году для разработки Ромашкинского месторождения',
            'category': 'tatneft',
            'date': '1950-11-24'
        },
        {
            'title': 'Сталинградская битва',
            'description': 'Крупнейшее сражение ВОВ (17.07.1942-02.02.1943), переломный момент войны',
            'category': 'war',
            'date': '1942-07-17'
        }
    ]
    
    for event in events:
        HistoricalEvent.objects.create(**event)

class Migration(migrations.Migration):
    dependencies = [
        ('assistant', '0001_initial'), # Зависимость от первой миграции
    ]
    
    operations = [
        migrations.RunPython(add_initial_data)
    ]