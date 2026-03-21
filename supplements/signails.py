from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from supplements.models import ImageSupplement, HomeBanner, FeedbackImage



def handle_image_cleanup(instance, model_class, field_name, action):
    if action == "delete":
        file_field = getattr(instance, field_name, None)

        if file_field:
            file_field.delete(save=False)


    elif action == "update":
        if not instance.pk:
            return
        try:
            old_instance = model_class.objects.get(pk=instance.pk)
        except model_class.DoesNotExist:
            return
        old_file = getattr(old_instance, field_name, None)
        new_file = getattr(instance, field_name,None)

        if old_file and old_file != new_file:
            old_file.delete(save=False)

           
@receiver(post_delete, sender=ImageSupplement)
def image_supplement_post_delete(sender, instance, **kwargs):
    handle_image_cleanup(instance, sender, "photo", action="delete")


@receiver(pre_save, sender=ImageSupplement)
def image_supplement_pre_save(sender, instance, **kwargs):
    handle_image_cleanup(instance, sender, "photo", action="update")



@receiver(post_delete, sender=HomeBanner)
def image_homebanner_post_delete(sender, instance, **kwargs):
    handle_image_cleanup(instance, sender, "image", action="delete")


@receiver(pre_save, sender=HomeBanner)
def image_homebanner_pre_save(sender, instance, **kwargs):
    handle_image_cleanup(instance, sender, "image", action="update")

@receiver(post_delete, sender=FeedbackImage)
def image_homebanner_pre_save(sender, instance, **kwargs):
    handle_image_cleanup(instance, sender, "image", action="delete")
