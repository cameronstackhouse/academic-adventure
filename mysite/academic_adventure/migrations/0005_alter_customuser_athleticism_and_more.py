# Generated by Django 4.0.1 on 2022-03-15 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic_adventure', '0004_alter_event_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='athleticism',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='intelligence',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='sociability',
            field=models.FloatField(default=0),
        ),
    ]
