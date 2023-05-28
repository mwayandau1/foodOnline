from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE, null=True, )
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.vendor_name


    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Vendor.objects.get(pk=self.pk)
            email_template = 'accounts/emails/admin_approval_email.html'
            context = {
                'user': self.user,
                'is_approved': self.is_approved
            }
            if original.is_approved != self.is_approved:
                if self.is_approved == True:
                    #Send notification to the vendor
                    mail_subject = "Congratulations! You restaurant has been approved for service"

                    send_notification(mail_subject, email_template, context)
                else:
                    mail_subject = "Sorry, Your restaurant has not been approved for service"

                    send_notification(mail_subject, email_template, context)
        return super(Vendor, self).save(*args, **kwargs)