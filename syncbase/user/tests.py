import unittest

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from lxml import etree


class UserUrlTestCase(TestCase):
    """ Test for the user app """

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user("_test")

    def test_can_reverse_url(self):
        """ The required url are defined """
        self.assertTrue(reverse('user:login'))
        self.assertTrue(reverse('user:logout'))
        self.assertTrue(reverse('user:password_change'))
        self.assertTrue(reverse('user:password_change_done'))
        self.assertTrue(reverse('user:password_reset')) # ask for pw reset
        self.assertTrue(reverse('user:password_reset_done')) # email sent
        self.assertTrue(reverse('user:password_reset_confirm',
            kwargs={'uidb64':'userid','token':'to-ken'})) # back from email
        self.assertTrue(reverse('user:password_reset_complete')) # reset done

    def test_login_view(self):
        """ The view display a form with username and password fields """
        rep = self.client.get(reverse('user:login'))
        # No need to continue if we don't get a 200 OK
        self.assertEqual(rep.status_code, 200)
        # Use xpath to check presence of element
        doc = etree.HTML(rep.content)
        self.assertEqual(len(doc.findall('.//input[@name="username"]')), 1)
        self.assertEqual(len(doc.findall('.//input[@name="password"]')), 1)

    def test_logout_view(self):
        """ The view don't have a user logged in """
        # TODO: check logout of user. Maybe not possible
        rep = self.client.get(reverse('user:logout'))
        # View need to return a response
        self.assertEqual(rep.status_code, 200)
        # There is a link back to login
        doc = etree.HTML(rep.content)
        login_url = reverse('user:login')
        self.assertTrue(doc.findall('.//a[@href="{}"]'.format(login_url)))

    def test_password_change_view_not_logged(self):
        """ Redirect the user to the login form """
        rep = self.client.get(reverse('user:password_change'), follow=True)
        # We follow link and end up with a valid page
        self.assertEqual(rep.status_code, 200)
        # Check we are redirected to the login page
        self.assertTrue(rep.redirect_chain[0], (reverse('user:login'), 302))

    def test_password_change_view_logged(self):
        """ Display a form with old_password, new_password1&2  """
        self.client.force_login(self.test_user)
        rep = self.client.get(reverse('user:password_change'))
        # check status code
        self.assertEqual(rep.status_code, 200)
        # xpath to check node
        doc = etree.HTML(rep.content)
        print(rep.content)
        self.assertEqual(len(doc.findall('.//input[@name="old_password"]')), 1)
        self.assertEqual(len(doc.findall('.//input[@name="new_password1"]')),1)
        self.assertEqual(len(doc.findall('.//input[@name="new_password2"]')),1)

    def test_password_change_view_done_not_logged(self):
        """ Redirect the user to the login form """
        rep = self.client.get(reverse('user:password_change'), follow=True)
        # We follow link and end up with a valid page
        self.assertEqual(rep.status_code, 200)
        # Check we are redirected to the login page
        self.assertTrue(rep.redirect_chain[0], (reverse('user:login'), 302))

    def test_password_change_view_done_not_logged(self):
        """ Confirm password change """
        # TODO check if password have been changed?
        self.client.force_login(self.test_user)
        rep = self.client.get(reverse('user:password_change_done'))
        # check status code
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, "Password change successful")

    def test_password_reset_view(self):
        """ Display a form with an email field """
        rep = self.client.get(reverse('user:password_reset'))
        # check status code
        self.assertEqual(rep.status_code, 200)
        # xpath to check node
        doc = etree.HTML(rep.content)
        self.assertEqual(len(doc.findall('.//input[@name="email"]')), 1)

    def test_password_reset_confirm_view(self):
        """ Say an email have been sent """
        rep = self.client.get(reverse('user:password_reset_done'))
        # check status code
        self.assertEqual(rep.status_code, 200)
        self.assertContains(rep, "link")
        self.assertContains(rep, "reset")
        self.assertContains(rep, "spam")

    @unittest.skip("Need a valid token to display the form")
    def test_reset_form_view_good_token(self):
        """ Display a form for a new password """
        #TODO get a real token to get a real form
        rep = self.client.get(reverse('user:password_reset_confirm',
            kwargs={'uidb64':"MQ", 'token':"4e7-e4752bc4379007ca4881"}))
        # check status code
        self.assertEqual(rep.status_code, 200)
        # xpath to check node
        doc = etree.HTML(rep.content)
        self.assertEqual(len(doc.findall('.//input[@name="new_password1"]')),1)
        self.assertEqual(len(doc.findall('.//input[@name="new_password2"]')),1)

    def test_reset_form_view_bad_token(self):
        """ Give a link to reset password """
        rep = self.client.get(reverse('user:password_reset_confirm',
            kwargs={'uidb64':"TST", 'token':"40-4"}))
        # check status code
        self.assertEqual(rep.status_code, 200)
        # xpath to check node
        doc = etree.HTML(rep.content)
        url = reverse('user:password_reset')
        self.assertTrue(doc.findall('.//a[@href="{}"]'.format(url)))

    def test_reset_form_done_view(self):
        """ Display a link to login """
        rep = self.client.get(reverse('user:password_reset_complete'))
        # View need to return a response
        self.assertEqual(rep.status_code, 200)
        # There is a link back to login
        doc = etree.HTML(rep.content)
        login_url = reverse('user:login')
        self.assertTrue(doc.findall('.//a[@href="{}"]'.format(login_url)))

