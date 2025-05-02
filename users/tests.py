from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from users.models import UserProfile
from users.forms import UserRegisterForm, ProfileForm
from users import views
from home.models import ContactMessage
from shop.models import Order


# --- VIEWS TESTING --- #

class UsersViewsTests(TestCase):
    """
    Test the views in the users app to ensure profile and order pages
    load correctly and handle forms and data updates.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass', email='test@example.com')
        self.profile = self.user.profile
        self.client.login(username='testuser', password='testpass')

    def test_profile_view_get(self):
        """
        Test that the profile page loads for logged-in user.
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_order_detail_view(self):
        """
        Test that order detail view loads for the correct user.
        """
        order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address_line1='4124 Street',
            city='Dublin',
            eir_code='A12B15',
            country='Ireland'
        )
        response = self.client.get(
            reverse('order_detail', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/order_detail.html')

    def test_delete_contact_message(self):
        """
        Test that user can delete their contact message.
        """
        message = ContactMessage.objects.create(
            user=self.user,
            name='User',
            email='user@example.com',
            message='Delete'
        )
        response = self.client.post(
            reverse('delete_contact_message', args=[message.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('profile'))
        self.assertFalse(ContactMessage.objects.filter(id=message.id).exists())


# --- URLS TESTING --- #

class UsersUrlsTests(TestCase):
    """
    Test that user URLs are correctly mapped to the right views.
    """

    def test_profile_url_resolves(self):
        """
        Check if /profile/ resolves to profile_view.
        """
        url = reverse('profile')
        self.assertEqual(resolve(url).func, views.profile_view)

    def test_order_detail_url_resolves(self):
        """
        Check if /order/<order_number>/ resolves to order_detail.
        """
        url = reverse('order_detail', args=['1234abcd'])
        self.assertEqual(resolve(url).func, views.order_detail)

    def test_delete_contact_message_url_resolves(self):
        """
        Check if delete_contact_message resolves correctly.
        """
        url = reverse('delete_contact_message', args=[1])
        self.assertEqual(resolve(url).func, views.delete_contact_message)


# --- MODELS TESTING --- #

class UserProfileModelTest(TestCase):
    """
    Test that the user object resturns correct username for UserProfile.
    """

    def test_str_returns_username(self):
        user = User.objects.create_user(username='tester', password='1234')
        self.assertEqual(str(user.profile), "tester's Profile")


# --- FORMS TESTING --- #

class UserRegisterFormTest(TestCase):
    """
    Test that the user registration form works properly.
    """

    def test_valid_register_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_passwords_must_match(self):
        form_data = {
            'username': 'failuser',
            'email': 'fail@example.com',
            'password1': 'password1',
            'password2': 'password2'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class ProfileFormTest(TestCase):
    """
    Test the profile update form for validation and field handling.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester', email='tester@example.com', password='1234')

    def test_profile_form_loads_with_initial_data(self):
        form = ProfileForm(user=self.user)
        self.assertEqual(form.fields['username'].initial, 'tester')
        self.assertEqual(form.fields['email'].initial, 'tester@example.com')
