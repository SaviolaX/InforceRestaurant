from django.db import models


class Restaurant(models.Model):
    """Restaurant db table"""
    title = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at', )
        
    def __str__(self) -> str:
        return self.title
