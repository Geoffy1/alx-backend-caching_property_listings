from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from .models import Property

@receiver(post_save, sender=Property)
def clear_property_cache_on_save(sender, instance, **kwargs):
    """
    Signal handler to clear the 'all_properties' cache key
    after a Property is created or updated.
    """
    print("Property saved. Clearing 'all_properties' cache...")
    cache.delete('all_properties')

@receiver(post_delete, sender=Property)
def clear_property_cache_on_delete(sender, instance, **kwargs):
    """
    Signal handler to clear the 'all_properties' cache key
    after a Property is deleted.
    """
    print("Property deleted. Clearing 'all_properties' cache...")
    cache.delete('all_properties')