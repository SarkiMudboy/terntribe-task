from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Cause, Donation


class CauseSerializer(serializers.ModelSerializer):

    image_url = serializers.URLField(
        max_length=2000, min_length=None, allow_blank=False
    )
    title = serializers.CharField(
        max_length=2000,
        validators=[UniqueValidator(queryset=Cause.objects.all())],
    )

    class Meta:
        model = Cause
        fields = ["id", "title", "description", "image_url"]
        read_only_fields = ["id"]


class ContributionSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    amount = serializers.DecimalField(
        coerce_to_string=False, max_digits=4, decimal_places=2
    )

    class Meta:
        model = Donation
        fields = ["id", "name", "email", "amount"]
        read_only_fields = ["id"]

    def save(self, cause: Cause) -> Donation:

        return Donation.objects.create(cause=cause, **self.validated_data)
