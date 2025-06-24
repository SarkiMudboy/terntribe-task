from django.db import models
from django.utils import timezone
import uuid


class TimestampUUIDMixin(models.Model):
    """Mixin model that provides id (as uuid), timestamps for entities"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Cause(TimestampUUIDMixin):

    title = models.CharField(max_length=2000, unique=True)
    description = models.TextField(max_length=5000)
    image_url = models.URLField(max_length=2000)

    def __str__(self) -> str:
        return self.title


class Donation(TimestampUUIDMixin):

    cause = models.ForeignKey(
        Cause, related_name="donations", on_delete=models.DO_NOTHING
    )
    name = models.CharField("Donor's name", max_length=2000)
    email = models.EmailField("Donor's email", max_length=2000)
    amount = models.DecimalField(
        "Amount donated", max_digits=4, decimal_places=2
    )

    def __str__(self) -> str:
        return f"{self.name} - {str(self.amount)}"
