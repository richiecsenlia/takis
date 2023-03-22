from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import MataKuliah, TeachingAssistantProfile

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

        TeachingAssistantProfile.objects.create(
            user = self.ta_user_1,
            nama = 'Immanuel Nadeak',
            kontrak = 'Part Time',
            status = 'Lulus S1',
            prodi = 'Ilmu Komputer'
        )

        TeachingAssistantProfile.objects.create(
            user = self.ta_user_2,
            nama = 'Virdian Harun',
            kontrak = 'Part Time',
            status = 'Lulus S1',
            prodi = 'Sistem Informasi'
        )

        MataKuliah.objects.create(nama='Aljabar Linear')
        MataKuliah.objects.create(nama='Basis Data')
        MataKuliah.objects.create(nama='Jaringan Komputer')
        MataKuliah.objects.create(nama='Rekayasa Perangkat Lunak')
        MataKuliah.objects.create(nama='Proyek Perangkat Lunak')

    def test_total_mata_kuliah(self):
        all_matkul = MataKuliah.objects.all()

        self.assertEquals(all_matkul.count(), 5)

    def test_total_ta_profile(self):
        all_profil_ta = TeachingAssistantProfile.objects.all()

        self.assertEquals(all_profil_ta.count(), 2)

    def test_ta_profile_name(self):
        ta_1 = TeachingAssistantProfile.objects.get(id=1)
        ta_2 = TeachingAssistantProfile.objects.get(id=2)

        self.assertEquals(str(ta_1), 'Immanuel Nadeak')
        self.assertEquals(str(ta_2), 'Virdian Harun')
