from cms.models.pages import (
    HomePage, IndexPage, OrganisationIndexPage, OrganisationPage,
    PersonIndexPage, PersonPage, RichTextPage
)
from wagtail.tests.utils import WagtailPageTests


class TestHomePage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(
            HomePage, {
                IndexPage, OrganisationIndexPage, PersonIndexPage, RichTextPage
            })


class TestIndexPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(IndexPage, {IndexPage, RichTextPage})


class TestRichTextPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(RichTextPage, {})


class TestPersonIndexPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(PersonIndexPage, {PersonPage})


class TestPersonPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(PersonPage, {})


class TestOrganisationIndexPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(
            OrganisationIndexPage, {OrganisationPage})


class TestOrganisationPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(OrganisationPage, {})
