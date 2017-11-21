from cms.models.pages import (
    BlogIndexPage, BlogPost, HomePage, IndexPage, OrganisationIndexPage,
    OrganisationPage, PersonIndexPage, PersonPage, RichTextPage, WorkIndexPage,
    WorkPage, _paginate
)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory, TestCase
from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Site
from sup.models import PublicationIdeaPage


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
                BlogIndexPage, IndexPage, OrganisationIndexPage,
                PublicationIdeaPage, PersonIndexPage, RichTextPage,
                WorkIndexPage
            })


class TestIndexPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(
            IndexPage, {IndexPage, RichTextPage, PublicationIdeaPage})


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

    def test_get_index_page(self):
        post = WorkPage.objects.first()
        expected = WorkIndexPage.objects.get(url_path='/home/our-work/')

        self.assertEqual(expected, post.get_index_page())


class TestBlogIndexPage(WagtailPageTests):
    fixtures = ['tests.json']

    def setUp(self):
        self.bip = BlogIndexPage.objects.get(url_path='/home/blog/')

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(
            BlogIndexPage, {BlogPost})

    def test_posts(self):
        self.assertEqual(2, self.bip.posts.count())

    def test_all_posts(self):
        factory = RequestFactory()

        request = factory.get('/home/blog/')
        request.site = Site.find_for_request(request)
        request.user = User.objects.create_user(username='test')

        response = self.bip.all_posts(request)
        self.assertEqual(200, response.status_code)

    def test_tag(self):
        factory = RequestFactory()

        request = factory.get('/home/blog/tag/news/')
        request.site = Site.find_for_request(request)
        request.user = User.objects.create_user(username='test')

        response = self.bip.tag(request)
        self.assertEqual(200, response.status_code)


class TestBlogPage(WagtailPageTests):
    fixtures = ['tests.json']

    def test_subpage_types(self):
        self.assertAllowedSubpageTypes(BlogPost, {})

    def test_get_index_page(self):
        post = BlogPost.objects.first()
        expected = BlogIndexPage.objects.get(url_path='/home/blog/')

        self.assertEqual(expected, post.get_index_page())


class TestSearch(TestCase):
    fixtures = ['tests.json']

    def setUp(self):
        self.client = Client()

    def test_search_url_name(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(200, response.status_code)

    def test_search_no_results(self):
        response = self.client.get(reverse('search'))
        self.assertIsNone(response.context[-1]['search_query'])
        self.assertEqual(
            0, response.context[-1]['search_results'].paginator.count)

        q = ''
        response = self.client.get(reverse('search'), {'q': q})
        self.assertEqual(q, response.context[-1]['search_query'])
        self.assertEqual(
            0, response.context[-1]['search_results'].paginator.count)

        q = 'missing'
        response = self.client.get(reverse('search'), {'q': q})
        self.assertEqual(q, response.context[-1]['search_query'])
        self.assertEqual(
            0, response.context[-1]['search_results'].paginator.count)

    def test_search_with_results(self):
        q = 'atlantic'
        response = self.client.get(reverse('search'), {'q': q})
        self.assertEqual(q, response.context[-1]['search_query'])
        self.assertEqual(
            1, response.context[-1]['search_results'].paginator.count)

        q = 'blog'
        response = self.client.get(reverse('search'), {'q': q})
        self.assertEqual(q, response.context[-1]['search_query'])
        self.assertEqual(
            1, response.context[-1]['search_results'].paginator.count)
