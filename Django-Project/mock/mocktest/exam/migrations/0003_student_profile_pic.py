# Generated by Django 4.1.7 on 2023-02-26 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_student_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]