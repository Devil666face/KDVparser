# Generated by Django 4.1.3 on 2022-11-17 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_alter_good_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='href',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='good',
            name='title',
            field=models.CharField(db_index=True, max_length=512),
        ),
    ]
