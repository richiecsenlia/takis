from django.test import TestCase
from django.contrib.auth.models import User

def create_daftar_matkul():
    MataKuliah.objects.create(nama='Aljabar Linear')
    MataKuliah.objects.create(nama='Basis Data')
    MataKuliah.objects.create(nama='Jaringan Komputer')
    MataKuliah.objects.create(nama='Rekayasa Perangkat Lunak')
    MataKuliah.objects.create(nama='Proyek Perangkat Lunak')


class AccountsModelTest(TestCase):
    
    def setUp(self):
        self.ta_user_1 = User.objects.create_user(
            username = 'testta1',
            password = 'ta123',
            email = 'testta1@example.com'
        )
        self.ta_user_1.role.role = 'TA'
        self.ta_user_1.role.save()

        self.ta_user_2 = User.objects.create_user(
            username = 'testta2',
            password = 'ta123',
            email = 'testta2@example.com'
        )
        self.ta_user_2.role.role = 'TA'
        self.ta_user_2.role.save()

        create_daftar_matkul()

    def test_create_ta_profile(self):
        ta_1_profile = TeachingAssistantProfile.objects.create(
            user = self.ta_user_1
            nama = 'Immanuel Nadeak',
            kontrak = 'Part Time',
            status = 'Lulus S1',
            prodi = 'Ilmu Komputer',
            matkul = '',
        )

        ta_2_profile = TeachingAssistantProfile.objects.create(
            user = self.ta_user_2
            nama = 'Virdian Harun',
            kontrak = 'Part Time',
            status = 'Lulus S1',
            prodi = 'Sistem Informasi',
            matkul = '',
        )

        self.assertEquals(str(ta_1_profile), 'Immanuel Nadeak')
        self.assertEquals(str(ta_2_profile), 'Virdian Harun')

    def test_get_all_ta_profile(self):
        list_profil_ta = TeachingAssistantProfile.objects.all()

        self.assertEquals(list_profil_ta.count(), 2)