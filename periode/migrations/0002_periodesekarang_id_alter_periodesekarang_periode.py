# Generated by Django 4.1 on 2023-05-08 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('periode', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodesekarang',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='periodesekarang',
            name='periode',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='periode.periode'),
        ),
    ]
