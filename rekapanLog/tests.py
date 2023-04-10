from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth.models import User
from .views import *
from pengisianLog.models import LogTA

# Create your tests here.
class RekapanLogTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.ta_user = User.objects.create(username='ta', password='ta', email='ta@ta.com')
        self.ta_user.role.role = 'TA'
        self.ta_user.role.save()

        LogTA.objects.create(
            user = self.ta_user,
            kategori = "Penyelenggaraan Kuliah",
            jenis_pekerjaan = "Membuat Soal",
            detail_kegiatan = "Essay dan Pilgan",
            pemberi_tugas = "Ibu Ika Alfina",
            uraian = "Membuat soal PR",
            periode = "Semester Kuliah",
            bulan_pengerjaan = "MAR",
            jumlah_rencana_kinerja = 4,
            satuan_rencana_kinerja = "Tugas",
            konversi_jam_rencana_kinerja = 1,
            jumlah_realisasi_kinerja = 0,
            satuan_realisasi_kinerja = "",
            konversi_jam_realisasi_kinerja = 0
        )

        LogTA.objects.create(
            user = self.ta_user,
            kategori = "Penyelenggaraan Kuliah",
            jenis_pekerjaan = "Koreksi Tugas",
            detail_kegiatan = "Essay dan Pilgan",
            pemberi_tugas = "Ibu Ika Alfina",
            uraian = "Mengoreksi PR",
            periode = "Semester Kuliah",
            bulan_pengerjaan = "APR",
            jumlah_rencana_kinerja = 2,
            satuan_rencana_kinerja = "Tugas",
            konversi_jam_rencana_kinerja = 0.5,
            jumlah_realisasi_kinerja = 0,
            satuan_realisasi_kinerja = "",
            konversi_jam_realisasi_kinerja = 0
        )

        LogTA.objects.create(
            user = self.ta_user,
            kategori = "Persiapan Kuliah",
            jenis_pekerjaan = "Mempersiapkan Environment",
            detail_kegiatan = "SCELE",
            pemberi_tugas = "Ibu Putu",
            uraian = "Rapat persiapan",
            periode = "Adhoc",
            bulan_pengerjaan = "SEP",
            jumlah_rencana_kinerja = 2,
            satuan_rencana_kinerja = "Tugas",
            konversi_jam_rencana_kinerja = 2,
            jumlah_realisasi_kinerja = 0,
            satuan_realisasi_kinerja = "",
            konversi_jam_realisasi_kinerja = 0
        )

    def test_get_average_all_rencana(self):
        rencanaAvg = get_all_rencana(self.ta_user)
        # penyelenggaraan harusnya 0.25, persiapan harusnya 0.33 (rata2)

        self.assertEquals(rencanaAvg['penyelenggaraan'], 0.25)
        self.assertEquals(rencanaAvg['persiapan'], (1/3))

