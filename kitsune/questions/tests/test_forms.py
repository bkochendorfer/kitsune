from collections import OrderedDict

from django.contrib.auth.models import AnonymousUser

from kitsune.questions.forms import NewQuestionForm, WatchQuestionForm
from kitsune.questions.tests import TestCaseBase
from kitsune.users.tests import UserFactory


class WatchQuestionFormTests(TestCaseBase):
    """Tests for WatchQuestionForm."""

    def test_anonymous_watch_with_email(self):
        form = WatchQuestionForm(
            AnonymousUser(), data={"email": "wo@ot.com", "event_type": "reply"}
        )
        assert form.is_valid()
        self.assertEqual("wo@ot.com", form.cleaned_data["email"])

    def test_anonymous_watch_without_email(self):
        form = WatchQuestionForm(AnonymousUser(), data={"event_type": "reply"})
        assert not form.is_valid()
        self.assertEqual("Please provide an email.", form.errors["email"][0])

    def test_registered_watch_with_email(self):
        form = WatchQuestionForm(UserFactory(), data={"email": "wo@ot.com", "event_type": "reply"})
        assert form.is_valid()
        assert not form.cleaned_data["email"]

    def test_registered_watch_without_email(self):
        form = WatchQuestionForm(UserFactory(), data={"event_type": "reply"})
        assert form.is_valid()


class TestNewQuestionForm(TestCaseBase):
    """Tests for the NewQuestionForm"""

    def setUp(self):
        super(TestNewQuestionForm, self).setUp()

    def test_metadata_keys(self):
        """Test metadata_field_keys property."""
        # Test the default form
        form = NewQuestionForm()
        expected = ["category", "useragent"]
        actual = form.metadata_field_keys
        self.assertEqual(expected, actual)

        # Test the form with a product
        product = {
            "key": "desktop",
            "name": "Firefox on desktop",
            "categories": OrderedDict(
                [
                    (
                        "cookies",
                        {
                            "name": "Cookies",
                            "topic": "cookies",
                            "tags": ["cookies"],
                        },
                    )
                ]
            ),
            "extra_fields": ["troubleshooting", "ff_version", "os"],
        }
        form = NewQuestionForm(product=product)
        expected = ["troubleshooting", "ff_version", "os", "useragent", "category"]
        actual = form.metadata_field_keys
        self.assertEqual(sorted(expected), sorted(actual))

    def test_cleaned_metadata(self):
        """Test the cleaned_metadata property."""
        # Test with no metadata
        data = {"title": "Lorem", "content": "ipsum", "email": "t@t.com"}
        product = {
            "key": "desktop",
            "name": "Firefox on desktop",
            "categories": OrderedDict(
                [
                    (
                        "cookies",
                        {
                            "name": "Cookies",
                            "topic": "cookies",
                            "tags": ["cookies"],
                        },
                    )
                ]
            ),
            "extra_fields": ["troubleshooting", "ff_version", "os"],
        }
        form = NewQuestionForm(product=product, data=data)
        form.is_valid()
        expected = {}
        actual = form.cleaned_metadata
        self.assertEqual(expected, actual)

        # Test with metadata
        data["os"] = "Linux"
        form = NewQuestionForm(product=product, data=data)
        form.is_valid()
        expected = {"os": "Linux"}
        actual = form.cleaned_metadata
        self.assertEqual(expected, actual)

        # Add an empty metadata value
        data["ff_version"] = ""
        form = NewQuestionForm(product=product, data=data)
        form.is_valid()
        expected = {"os": "Linux"}
        actual = form.cleaned_metadata
        self.assertEqual(expected, actual)
