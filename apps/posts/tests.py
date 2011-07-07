from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from forms import PostForm

# Test post form object
class PostFormTest(TestCase):
    def test_no_author(self):
        form = PostForm({'title' : 'This is title', 'content' : 'This is content'})
        self.assertFalse(form.is_valid())
    def test_no_title(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'content' : 'This is content','author' : author})
        self.assertFalse(form.is_valid())
    def test_no_content(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is title', 'author' : author})
        self.assertFalse(form.is_valid())
    def test_author_title_content(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         'author' : author})
        self.assertTrue(form.is_valid())
    def test_duplicated_content_regardless_author(self): 
        author = User.objects.get(username = 'kecebongsoft')
        form1 = PostForm({'title' : 'This is title', 'content' : 'This is content',
                          'author' : author})
        
        form2 = PostForm({'title' : 'This is title', 'content' : 'This is content',
                          'author' : author})

        self.assertTrue(form1.is_valid())
        form1.save()

        self.assertFalse(form2.is_valid())
        pass

class PostTest(TestCase):
    def test_new_post(self):
        c = Client()
        c.login(username = 'kecebongsoft', password='123')
        response = self.client.post(
            reverse('posts:new'),
            {
                'title' : 'This is title',
                'content' : 'This is content',
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_post(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         'author' : author})
        form.assertTrue(form.is_valid())
        post = form.save()

        c = Client()
        c.login(username = 'kecebongsoft', password='123')
        response = self.client.post(
            reverse('posts:edit'),
            {
                'title' : 'This is another title',
                'content' : 'This is another content',
                'post_id' : post.id,
            }
        )
        self.assertEqual(response.status_code, 200)
    def test_edit_post_different_user_admin(self):
        author = User.objects.get(username = 'kecebongsoft')

        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         'author' : author})
        self.assertTrue(form.is_valid())
        post = form.save()

        c = Client()
        c.login(username = 'admin', password='123')
        response = self.client.post(
            reverse('posts:edit'),
            {
                'title' : 'This is another title',
                'content' : 'This is another content',
                'post_id' : post.id,
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_post_different_user_normal(self):
        author = User.objects.get(username = 'kecebongsoft')

        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         'author' : author})
        self.assertTrue(form.is_valid())
        post = form.save()

        c = Client()
        c.login(username = 'dedi', password='123')
        response = self.client.post(
            reverse('posts:edit'),
            {
                'title' : 'This is another title',
                'content' : 'This is another content',
                'post_id' : post.id,
            }
        )
        self.assertEqual(response.status_code, 500)