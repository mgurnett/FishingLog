from django.db import models
        
class Conference(models.Model):
    name = models.CharField(max_length = 100)
    nhl_id = models.IntegerField ()
    
    class Meta:
        ordering = ['name']

    def __str__ (self):
        return self.name
        
class Division(models.Model):
    name = models.CharField(max_length = 100)
    nhl_id = models.IntegerField ()
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['name']

    def __str__ (self):
        return self.name
        
class Team(models.Model):
    name = models.CharField(max_length = 100)
    nhl_id = models.IntegerField ()
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    venue = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    teamName = models.CharField(max_length = 100)
    locationName = models.CharField(max_length = 100)
    
    class Meta:
        ordering = ['name']

    def __str__ (self):
        return self.name
        
class Player(models.Model):
    firstName = models.CharField(max_length = 100)
    lastName = models.CharField(max_length = 100)
    nhl_id = models.IntegerField ()
    jersey = models.IntegerField ()
    birthDate = models.DateTimeField()
    nationality = models.CharField(max_length = 100)
    height = models.CharField(max_length = 100)
    weight = models.CharField(max_length = 100)
    active = models.BooleanField()
    alternateCaptain = models.BooleanField()
    captain = models.BooleanField()
    rookie = models.BooleanField()
    shootsCatches = models.CharField(max_length = 100)
    rosterStatus = models.CharField(max_length = 10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    primaryPosition = models.CharField(max_length = 100)

    class Meta:
        ordering = ['jersey']

    def __str__ (self):
        return (f'{self.lastName}, {self.firstName} ({self.jersey})')