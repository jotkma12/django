from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Ingreso, Gasto
from .utils import generarBalances

@receiver(post_save, sender=Ingreso)
@receiver(post_save, sender=Gasto)
@receiver(post_delete, sender=Ingreso)
@receiver(post_delete, sender=Gasto)
def actualizarBalance(sender, instance, **kwargs):
    generarBalances()
    