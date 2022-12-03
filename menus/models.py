from django.db import models

from restaurants.models import Restaurant


class Menu(models.Model):
    """Menu db table"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    file = models.FileField(upload_to='menus/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )
        
    def __str__(self) -> str:
        return '{0}: {1}'.format(self.title, self.restaurant.title)
    
