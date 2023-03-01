from django.db import models
from django.utils.timezone import now


# Create your models here.


class Text(models.Model):
    sno = models.AutoField(primary_key=True)
    input_text = models.TextField()
    summary_output = models.TextField()
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return ' (' + str(self.sno)+') ' + self.input_text[:50] + '...' + '  (summarize on : ' + str(self.timeStamp)+ ' )'
