# Generated by Django 4.2.16 on 2024-11-26 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objectdetection', '0002_objectdetectionimage_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='objectdetectionimage',
            old_name='image',
            new_name='objectdetection_image',
        ),
    ]
