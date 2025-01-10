from django.db import models

class Trucking(models.Model):

    day = models.CharField(max_length=10)
    air_line_code = models.CharField(max_length=3)
    flight_number = models.CharField(max_length=4)
    departure_time = models.TimeField()
    distance = models.DecimalField(max_digits=10, decimal_places=0)  # Distance in kilometers or miles
    travel_time = models.TimeField(verbose_name="Reistijd") # Travel time as a duration (hours, minutes, seconds)
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    operator = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.air_line_code} {self.flight_number}"

class Members(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    function = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    