from cms.models.pages import (
    HomePage, IndexPage, OrganisationIndexPage, OrganisationPage,
    PersonIndexPage, PersonPage, RichTextPage, WorkIndexPage, WorkPage,
    _paginate
)
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Site


class TestPages(TestCase):

    def test__paginate(self):
        items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

        factory = RequestFactory()

        request = factory.get('/test?page=1')
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                         _paginate(request, items).object_list)
        request = factory.get('/test?page=2')
        self.assertEqual([10, 11, 12, 13, 14, 15, 16, 17],
                         _paginate(request, items).object_list)
        request = factory.get('/test?page=10')
        self.assertEqual([10, 11, 12, 13, 14, 15, 16, 17],
                         _paginate(request, items).object_list)
        request = factory.get('/test?page=a')
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                         _paginate(request, items).object_list)


class TestHomePage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(
            HomePage, {
                IndexPage, OrganisationIndexPage, PersonIndexPage,
                RichTextPage, WorkIndexPage
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


class TestWorkIndexPage(WagtailPageTests):
    fixtures = ['tests.json']

    def setUp(self):
        self.wip = WorkIndexPage.objects.get(url_path='/home/our-work/')

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(
            WorkIndexPage, {WorkPage})

    def test_works(self):
        self.assertEqual(2, self.wip.works.count())

    def test_tag(self):
        factory = RequestFactory()

        request = factory.get('/home/our-work/tag/site/')
        request.site = Site.find_for_request(request)
        request.user = User.objects.create_user(username='test')

        response = self.wip.tag(request)
        self.assertEqual(200, response.status_code)


class TestWorkPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(WorkPage, {})
