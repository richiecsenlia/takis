# Generated by Django 4.1.7 on 2023-05-12 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_teachingassistantprofile_prodi'),
        ('periode', '0004_alter_periode_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='periode',
            name='daftar_ta',
            field=models.ManyToManyField(to='accounts.teachingassistantprofile'),
        ),
    ]
