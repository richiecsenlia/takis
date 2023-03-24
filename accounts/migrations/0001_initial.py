# Generated by Django 4.1.7 on 2023-03-23 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MataKuliah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TeachingAssistantProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50, verbose_name='Nama Lengkap')),
                ('kontrak', models.CharField(choices=[('Part Time', 'Part Time'), ('Full Time', 'Full Time')], max_length=20, verbose_name='Jenis Kontrak')),
                ('status', models.CharField(choices=[('Lulus S1', 'Lulus S1'), ('Lulus S2', 'Lulus S2'), ('Lulus S2 MTI', 'Lulus S2 MTI')], max_length=20, verbose_name='Status Kemahasiswaan')),
                ('prodi', models.CharField(choices=[('IK', 'Ilmu Komputer'), ('IK KKI', 'Ilmu Komputer KKI'), ('SI', 'Sistem Informasi'), ('TI', 'Teknologi Informasi')], max_length=30, verbose_name='Program Studi')),
                ('slug', models.SlugField(unique=True, verbose_name='URL Slug')),
                ('daftar_matkul', models.ManyToManyField(to='accounts.matakuliah')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
