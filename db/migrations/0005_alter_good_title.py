# Generated by Django 4.1.3 on 2022-11-17 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_good_coef'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='title',
            field=models.CharField(db_index=True, max_length=512, unique=True),
        ),
    ]
