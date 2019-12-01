# Generated by Django 2.2.7 on 2019-11-30 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('name', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'Families',
            },
        ),
    ]
