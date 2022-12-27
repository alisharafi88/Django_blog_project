from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import reverse


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user=User.objects.create(username='user1')
        cls.post=Post.objects.create(
            title='p1',
            text='p1 txt',
            status=Post.STATUS_CHOICES[0][0],
            author=cls.user,
        )
        cls.post2=Post.objects.create(
            title='p2',
            text='loremipsum2',
            status=Post.STATUS_CHOICES[1][0],
            author=cls.user,
        )

    def test_post_model_str(self):
        post = self.post
        self.assertEqual(str(post), f'{post.title}:{post.author}')



    def test_post_list_url_by_name(self):
        response=self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_url(self):
        response=self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        response=self.client.get(reverse('post_list'))
        self.assertContains(response, 'p1')

    def teste_post_details_on_blog_detail_page(self):
        response = self.client.get(f'/blog/{self.post.id}')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.text)

    def test_post_detail_url(self):
        response= self.client.get(f'/blog/{self.post.id}')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_by_name(self):
        response=self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_status_404_if_post_id_not_exist(self):
        response=self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_in_post_list(self):
        response=self.client.get(reverse('post_list'))
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'some title',
            'text': 'some text',
            'author': self.user.id,
            'status': 'pub',

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'some title')
        self.assertEqual(Post.objects.last().text, 'some text')
        # self.assertEqual(Post.objects.last().author, self.user.id)
        # self.assertEqual(Post.objects.last().title, 'pub')

    def test_post_update(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'updated title',
            'text': 'updated text',
            'author': self.post2.author.id,
            'status': 'pub',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'updated title')
        self.assertEqual(Post.objects.last().text, 'updated text')
        # self.assertEqual(Post.objects.last().author, self.post2.author.id)
        # self.assertEqual(Post.objects.last().title, 'pub')

    def test_post_delete(self):
        response = self.client.post(reverse('post_delete', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)
