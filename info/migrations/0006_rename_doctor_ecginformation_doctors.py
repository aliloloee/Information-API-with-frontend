# Generated by Django 3.2.3 on 2021-06-15 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0005_alter_ecginformation_nurse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ecginformation',
            old_name='doctor',
            new_name='doctors',
        ),
    ]