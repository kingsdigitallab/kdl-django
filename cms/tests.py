from cms.models.pages import HomePage, IndexPage, RichTextPage
from wagtail.tests.utils import WagtailPageTests


class TestHomePage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(HomePage, {IndexPage, RichTextPage})


class TestIndexPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(IndexPage, {IndexPage, RichTextPage})


class TestRichTextPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(RichTextPage, {})
