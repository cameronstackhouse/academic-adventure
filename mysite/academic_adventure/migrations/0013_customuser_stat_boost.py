# Generated by Django 4.0.1 on 2022-03-21 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic_adventure', '0012_alter_image_rarity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='stat_boost',
            field=models.BooleanField(default=False),
        ),
    ]
