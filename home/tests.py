from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from home.models import Testimonial, NewsletterSubscriber, ContactMessage
from home.forms import TestimonialForm, ContactForm, NewsletterSignupForm
from home import views


# --- VIEWS TESTING --- #


class HomeViewsTests(TestCase):
    """
    Test the views in the home app to make sure pages load correctly
    and forms behave as expected.
    """

    def setUp(self):
        """
        Set up a test client, test user, and logged-in session before each test
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass', email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass')

    def test_index_view_get(self):
        """
        Test that the homepage loads correctly using GET method.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_index_view_post_valid_form(self):
        """
        Test submitting a valid testimonial POST request to the homepage.
        """
        response = self.client.post(reverse('home'), {
            'name': 'Test User',
            'message': 'Great site!',
            'role': 'Tester'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testimonial')
        self.assertTrue(Testimonial.objects.exists())

    def test_contact_view_get(self):
        """
        Test that the contact page loads with a form using GET.
        """
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.html')

    def test_contact_view_post_valid_form(self):
        """
        Test submitting a valid POST request through the contact form.
        """
        response = self.client.post(reverse('contact'), {
            'name': 'Contact User',
            'email': 'contact@example.com',
            'message': 'Hello!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'successfully')
        self.assertTrue(ContactMessage.objects.exists())

    def test_newsletter_signup_view_success(self):
        """
        Test newsletter signup with a new valid email via POST (AJAX-style).
        """
        response = self.client.post(
            reverse('newsletter_signup'),
            content_type='application/json',
            data={'email': 'newuser@example.com'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})
        self.assertTrue(NewsletterSubscriber.objects.filter(
            email='newuser@example.com').exists())

    def test_newsletter_signup_duplicate_email(self):
        """
        Test newsletter signup fails if the email is already subscribed.
        """
        NewsletterSubscriber.objects.create(email='dupe@example.com')
        response = self.client.post(
            reverse('newsletter_signup'),
            content_type='application/json',
            data={'email': 'dupe@example.com'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': False,
            'message': 'This email is already subscribed.'
        })


# --- URLS TESTING --- #


class HomeUrlsTests(TestCase):
    """
    Test that each URL in the home app is connected to the correct view.
    """

    def test_home_url_resolves_to_index_view(self):
        """
        Checks if the root URL ('') uses the index view.
        """
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.index)

    def test_contact_url_resolves_to_contact_view(self):
        """
        Checks if '/contact/' URL uses the contact_view.
        """
        url = reverse('contact')
        self.assertEqual(resolve(url).func, views.contact_view)

    def test_about_url_resolves_to_about_view(self):
        """
        Checks if '/about/' URL uses the about view.
        """
        url = reverse('about')
        self.assertEqual(resolve(url).func, views.about)

    def test_newsletter_signup_url_resolves_correctly(self):
        """
        Checks if '/newsletter/signup/' URL uses the newsletter_signup view.
        """
        url = reverse('newsletter_signup')
        self.assertEqual(resolve(url).func, views.newsletter_signup)


# --- MODELS TESTING --- #


class TestimonialModelTest(TestCase):
    """
    Tests basic functionality of the Testimonial model.
    """

    def test_string_representation_returns_name(self):
        """
        Checks that the __str__ method returns the name.
        """
        testimonial = Testimonial.objects.create(
            name='John Doe',
            message='Great service!',
            role='Customer'
        )
        self.assertEqual(str(testimonial), 'John Doe')


class ContactMessageModelTest(TestCase):
    """
    Tests basic functionality of the ContactMessage model.
    """

    def test_string_representation_returns_name_and_email(self):
        """
        Checks that the __str__ method returns the correct format.
        """
        message = ContactMessage.objects.create(
            name='Jane Smith',
            email='jane@example.com',
            message='I have a question.'
        )
        self.assertEqual(
            str(message),
            'Message from Jane Smith (jane@example.com)')

    def test_contact_message_with_user(self):
        """
        Checks if a message can be linked to a user.
        """
        user = User.objects.create_user(username='testuser', password='pass')
        message = ContactMessage.objects.create(
            user=user,
            name='Test User',
            email='test@example.com',
            message='Hello!'
        )
        self.assertEqual(message.user.username, 'testuser')


class NewsletterSubscriberModelTest(TestCase):
    """
    Tests basic functionality of the NewsletterSubscriber model.
    """

    def test_string_representation_returns_email(self):
        """
        Checks that the __str__ method returns the email.
        """
        subscriber = NewsletterSubscriber.objects.create(
            email='sub@example.com')
        self.assertEqual(str(subscriber), 'sub@example.com')


# --- FORMS TESTING --- #


class TestimonialFormTest(TestCase):
    """
    Tests the TestimonialForm to ensure it accepts valid input
    and correctly handles optional and required fields.
    """

    def test_valid_testimonial_form(self):
        """
        A form with name and message (role is optional) should be valid.
        """
        form = TestimonialForm(data={
            'name': 'John Doe',
            'message': 'This is a great website!',
            'role': 'Customer'
        })
        self.assertTrue(form.is_valid())

    def test_missing_required_field(self):
        """
        A form missing the name should be invalid.
        """
        form = TestimonialForm(data={
            'message': 'Still a nice site!'
        })
        self.assertFalse(form.is_valid())


class ContactFormTest(TestCase):
    """
    Tests the ContactForm to make sure it validates required fields.
    """

    def test_valid_contact_form(self):
        """
        A form with name, email, and message should be valid.
        """
        form = ContactForm(data={
            'name': 'Alice',
            'email': 'alice@example.com',
            'message': 'I need help with an order.'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """
        A form with an invalid email should fail validation.
        """
        form = ContactForm(data={
            'name': 'Bob',
            'email': 'invalid-email',
            'message': 'Help me!'
        })
        self.assertFalse(form.is_valid())


class NewsletterSignupFormTest(TestCase):
    """
    Tests the NewsletterSignupForm to ensure valid email input is accepted.
    """

    def test_valid_newsletter_form(self):
        """
        A form with a valid email should be valid.
        """
        form = NewsletterSignupForm(data={'email': 'subscriber@example.com'})
        self.assertTrue(form.is_valid())

    def test_missing_email(self):
        """
        A form with no email should be invalid.
        """
        form = NewsletterSignupForm(data={})
        self.assertFalse(form.is_valid())
