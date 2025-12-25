from django.test import TestCase
from django.contrib.auth import get_user_model

class  UserAccountTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'Diho', 'Kelechi', 'password'
        )
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.user_name, 'Diho')
        self.assertEqual(super_user.first_name, 'Kelechi')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'Diho')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                'testuser@super.com', user_name='Diho', first_name='Kelechi', password='password', is_superuser=False
            )
        
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                'testuser@super.com', user_name='Diho', first_name='Kelechi', password='password', is_staff=False
            )
        
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', user_name='Diho', first_name='Kelechi', password='password', is_superuser=False
            )

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'Sopman', 'Sopuru', 'password'
        )
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.user_name, 'Sopman')
        self.assertEqual(user.first_name, 'Sopuru')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', user_name='Sopman', first_name='Sopuru', password='password'
            )
        