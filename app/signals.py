# from django.db.models.signals import post_save, m2m_changed
# from django.dispatch import receiver
# from .models import User, Item, Order


# # @receiver(post_save, sender=Order)
# @receiver(m2m_changed, sender=Order.items.through)
# def control_total_price(sender, instance, **kwargs):
#     # if created:
#     #     Item.objects.get(instance)
#     pass