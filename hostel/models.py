from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import HostelOwner

User = get_user_model()


class HostelCategory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class HostStateAddress(models.Model):
    state = models.CharField('استان', max_length=255)

    def __str__(self):
        return self.state


class Host(models.Model):
    cat = models.ForeignKey(HostelCategory, on_delete=models.CASCADE)
    owner = models.ForeignKey(HostelOwner, on_delete=models.CASCADE)
    reserved = models.BooleanField(default=False)
    chek_in_time = models.CharField(max_length=50)
    chek_out_time = models.CharField(max_length=50)
    max_number_guests = models.SmallIntegerField(default=2)


class HostAddress(models.Model):
    host = models.OneToOneField(Host, related_name="host_address", on_delete=models.CASCADE)
    state = models.OneToOneField(HostStateAddress, on_delete=models.RESTRICT)
    city = models.CharField('شهر', max_length=255)
    street = models.CharField('خیابان', max_length=255)
    alley = models.CharField('کوچه', max_length=255)
    number = models.CharField('پلاک', max_length=255)

    def __str__(self):
        return f"{self.city}-{self.street}-{self.alley}-{self.number}"


class HostImage(models.Model):
    host = models.ForeignKey(Host, related_name="host_image", on_delete=models.CASCADE)
    img = models.ImageField(upload_to="host/", null=True, blank=True)


class HostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host = models.ForeignKey(Host, related_name="host_comments", on_delete=models.CASCADE)
    rate = models.FloatField(
        validators=[MinValueValidator(0.0),  MaxValueValidator(5.0)])
    text = models.CharField(max_length=500)
