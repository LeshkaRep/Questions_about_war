from django.db import models

class HistoricalEvent(models.Model):
    WAR = 'war'
    TATNEFT = 'tatneft'
    
    CATEGORY_CHOICES = [
        (WAR, 'Великая Отечественная Война'),
        (TATNEFT, 'Татнефть'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
