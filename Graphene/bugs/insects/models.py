from django.db import models
from django.utils import timezone

class Bug(models.Model):    
    name = models.CharField ('Insect name', max_length=100)

    def __str__(self):
        return self.name

class Week(models.Model):
    number = models.IntegerField()

    def __str__ (self):
        return str(self.number)

class Temp(models.Model):
    name = models.CharField(max_length = 100)
    week_numbers = models.ManyToManyField(Week, through='Log')

    def __str__ (self):
        return self.name


class Bug_site(models.Model):
    date = models.DateField(default=timezone.now)
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="sightings")
    temp = models.ForeignKey(Temp, on_delete=models.CASCADE, related_name="recorded_temps")
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="weeks")

    def __str__ (self):
        return f'{self.bug.name} seen on {self.date}'


class Log(models.Model):
    note = models.CharField(max_length = 100)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="recorded_temps")
    temp = models.ForeignKey(Temp, on_delete=models.CASCADE, related_name="weeks")
    date = models.DateField(default=timezone.now)

    def __str__ (self):
        return self.note

STRENGTH = (
    (0, "none"),
    (1, "few"),
    (2, "weak"),
    (3, "low"),
    (4, "lots"),
    (5, "abundent"),
)


class Hatch(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="insect")
    week = models.ManyToManyField(Week, through = 'Strength')

    def __str__ (self):
        return f'{self.bug.name} are often found during the weeks of '


class Strength(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="week")
    hatch = models.ForeignKey(Hatch, on_delete=models.CASCADE, related_name="strength_of_hatch")
    strength = models.IntegerField ( 
        default = 0,
        choices = STRENGTH,
        )

    def __str__ (self):
        return f'bug: {self.hatch.bug.name} in week: {self.week.number} has a strength of: {self.strength}'

    '''
    ON DELETE CASCADE: if a row of the referenced table is deleted, then all matching rows 
    in the referencing table are deleted.
    ON DELETE SET NULL: if a row of the referenced table is deleted, then all referencing columns 
    in all matching rows of the referencing table to be set to null.
    on_delete=models.SET_NULL, null=True)
    ON DELETE SET DEFAULT: if a row of the referenced table is deleted, then all referencing 
    columns in all matching rows of the referencing table to be set to the column’s default value.
    on_delete=models.SET_DEFAULT, default=1)
    ON DELETE RESTRICT: it is prohibited to delete a row of the referenced table if that row 
    has any matching rows in the referencing table.
    ON DELETE NO ACTION (the default): there is no referential delete action; the referential 
    constraint only specifies a constraint check.
    NO DELETE PROTECT
    '''