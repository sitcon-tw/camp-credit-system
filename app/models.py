from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class team(models.Model):
    tid = models.CharField(max_length=32, validators=[alphanumeric], primary_key=True, verbose_name="Team ID", help_text="Alphanumeric name for the team.")
    name = models.CharField(max_length=32, null=True, name="Name", help_text="Name of the team.")
    points = models.IntegerField(verbose_name="Points", help_text="The current amount of points of this group.", default=0)
    modified_reason = models.TextField(verbose_name="Modified Reason", help_text="The reason of last modification.", null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.verbose_name) + ", currently has " + str(self.points) + " points."


class player(models.Model):
    user = models.OneToOneField(User, verbose_name="User", help_text="The user of this player.")
    team = models.ForeignKey(team, verbose_name="Team", help_text="The team this player belongs to.")
    points_acquired = models.IntegerField(verbose_name="Acquired Points", help_text="The amount of points acquired by this player.", default=0)
    secret = models.CharField(max_length=16, primary_key=True, default=get_random_string(16), verbose_name="Reg. Token", help_text="A token used to simplify the process of registration.")
    modified_reason = models.TextField(verbose_name="Modified Reason", help_text="The reason of last modification.", null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.user.get_full_verbose_name()) + " (" + str(self.user.get_username()) + "), acquired " + str(self.points_acquired) + " points for " + str(self.team.name) + ", which currently has " + str(self.team.points) + " points. \n The regiunicodeation token for this player is: " + str(self.secret) + " ."

class card(models.Model):
    cid = models.CharField(max_length=16, primary_key=True, default=get_random_string(16), verbose_name="Card ID", help_text="The unique ID for the points card.")
    value = models.IntegerField(default="1", verbose_name="Value", help_text="The value of the points card.")
    active = models.BooleanField(default=True, verbose_name="Active?")
    retrieved = models.BooleanField(default=False, verbose_name="Retrieved")
    name = models.CharField(max_length=32, verbose_name="Name", help_text="Name of the card.", null=True)
    long_desc = models.TextField(verbose_name="Descriptions", help_text="Long descriptions about the card.", null=True)
    modified_reason = models.TextField(verbose_name="Modified Reason", help_text="The reason of last modification.", null=True)
    history = HistoricalRecords()

    def __str__(self):
        if self.active:
            return str(self.name) + ", an active points card with " + str(self.value) + " points, with the cid: \"" + str(self.cid) + "\" ."
        else:
            return str(self.name) + ", an inactive points card with " + str(self.value) + " points, with the cid: \"" + str(self.cid) + "\" ."
