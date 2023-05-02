from django.db import models

class Cotacao(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateField()
    dolar = models.DecimalField(max_digits=5, decimal_places=2)
    euro = models.DecimalField(max_digits=5, decimal_places=2)
    yene = models.DecimalField(max_digits=5, decimal_places=2)
    real = models.DecimalField(max_digits=5, decimal_places=2)