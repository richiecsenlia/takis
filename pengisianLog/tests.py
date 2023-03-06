from django.test import TestCase
from .models import LogTA

# Create your tests here.
class PengisianLogTestCase(TestCase):

    def test_create_LogTA(self):
        logTA_1 = LogTA.objects.create(
            kategori = "Penyelenggaraan Kuliah",
            jenis_pekerjaan = "Membuat Soal",
            detail_kegiatan = "Essay dan Pilgan",
            pemberi_tugas = "Ibu Ika Alfina",
            uraian = "Membuat soal PR",
            periode = "Semester Kuliah",
            bulan_pengerjaan = "MAR",
            rencana_kinerja = 4
        )

        logTA_1 = LogTA.objects.create(
            kategori = "Persiapan Kuliah",
            jenis_pekerjaan = "Mempersiapkan Environment",
            detail_kegiatan = "SCELE",
            pemberi_tugas = "Ibu Putu",
            uraian = "Rapat persiapan",
            periode = "Adhoc",
            bulan_pengerjaan = "SEP",
            rencana_kinerja = 1
        )

        all_logTA = LogTA.objects.all()
        
        self.assertEquals(all_logTA.count(), 2)
        self.assertEquals(all_logTA[0].kategori, "Penyelenggaraan Kuliah")
        self.assertEquals(all_logTA[1].kategori, "Persiapan Kuliah")
