# Generated by Django 4.1.7 on 2023-05-25 13:52

from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalLogTA',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('kategori', models.CharField(choices=[('Dukungan Kuliah Kakak Asuh', 'Dukungan Kuliah Kakak Asuh'), ('Pengembangan Institusi', 'Pengembangan Institusi'), ('Penyelenggaraan Kuliah', 'Penyelenggaraan Kuliah'), ('Persiapan Kuliah', 'Persiapan Kuliah'), ('Riset dan Pusilkom', 'Riset dan Pusilkom')], max_length=30)),
                ('jenis_pekerjaan', models.CharField(max_length=20)),
                ('detail_kegiatan', models.CharField(max_length=100)),
                ('pemberi_tugas', models.CharField(max_length=20)),
                ('uraian', models.CharField(max_length=200)),
                ('periode', models.CharField(choices=[('Adhoc', 'Adhoc'), ('Bulanan', 'Bulanan'), ('Harian', 'Harian'), ('Semester Kuliah', 'Semester Kuliah'), ('Sepanjang Kontrak', 'Sepanjang Kontrak')], max_length=20)),
                ('bulan_pengerjaan', models.CharField(choices=[('JAN', 'JAN'), ('FEB', 'FEB'), ('MAR', 'MAR'), ('APR', 'APR'), ('MEI', 'MEI'), ('JUN', 'JUN'), ('JUL', 'JUL'), ('AGT', 'AGT'), ('SEP', 'SEP'), ('OKT', 'OKT'), ('NOV', 'NOV'), ('DES', 'DES')], max_length=20)),
                ('jumlah_rencana_kinerja', models.IntegerField()),
                ('satuan_rencana_kinerja', models.CharField(max_length=20)),
                ('konversi_jam_rencana_kinerja', models.FloatField()),
                ('jumlah_realisasi_kinerja', models.IntegerField(blank=True, default=0, null=True)),
                ('satuan_realisasi_kinerja', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('konversi_jam_realisasi_kinerja', models.FloatField(blank=True, default=0, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical log ta',
                'verbose_name_plural': 'historical log tas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='LogTA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kategori', models.CharField(choices=[('Dukungan Kuliah Kakak Asuh', 'Dukungan Kuliah Kakak Asuh'), ('Pengembangan Institusi', 'Pengembangan Institusi'), ('Penyelenggaraan Kuliah', 'Penyelenggaraan Kuliah'), ('Persiapan Kuliah', 'Persiapan Kuliah'), ('Riset dan Pusilkom', 'Riset dan Pusilkom')], max_length=30)),
                ('jenis_pekerjaan', models.CharField(max_length=20)),
                ('detail_kegiatan', models.CharField(max_length=100)),
                ('pemberi_tugas', models.CharField(max_length=20)),
                ('uraian', models.CharField(max_length=200)),
                ('periode', models.CharField(choices=[('Adhoc', 'Adhoc'), ('Bulanan', 'Bulanan'), ('Harian', 'Harian'), ('Semester Kuliah', 'Semester Kuliah'), ('Sepanjang Kontrak', 'Sepanjang Kontrak')], max_length=20)),
                ('bulan_pengerjaan', models.CharField(choices=[('JAN', 'JAN'), ('FEB', 'FEB'), ('MAR', 'MAR'), ('APR', 'APR'), ('MEI', 'MEI'), ('JUN', 'JUN'), ('JUL', 'JUL'), ('AGT', 'AGT'), ('SEP', 'SEP'), ('OKT', 'OKT'), ('NOV', 'NOV'), ('DES', 'DES')], max_length=20)),
                ('jumlah_rencana_kinerja', models.IntegerField()),
                ('satuan_rencana_kinerja', models.CharField(max_length=20)),
                ('konversi_jam_rencana_kinerja', models.FloatField()),
                ('jumlah_realisasi_kinerja', models.IntegerField(blank=True, default=0, null=True)),
                ('satuan_realisasi_kinerja', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('konversi_jam_realisasi_kinerja', models.FloatField(blank=True, default=0, null=True)),
            ],
        ),
    ]
