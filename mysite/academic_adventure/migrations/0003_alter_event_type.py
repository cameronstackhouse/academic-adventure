# Generated by Django 4.0.1 on 2022-02-28 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic_adventure', '0002_event_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('Battle', 'Battle'), ('Academic', 'Academic'), ('Sports', 'Sports'), ('Social', 'Social')], max_length=40),
        ),
    ]
