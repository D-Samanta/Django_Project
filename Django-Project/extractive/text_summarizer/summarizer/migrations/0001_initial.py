# Generated by Django 4.1.7 on 2023-02-22 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('input_text', models.TextField()),
                ('summary_output', models.TextField()),
                ('timeStamp', models.DateTimeField(blank=True)),
            ],
        ),
    ]