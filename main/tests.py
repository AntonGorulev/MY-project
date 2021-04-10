from django.test import TestCase


class ArticleTestCase(TestCase):

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.content.decode('utf-8'), 'MY project!')
    
    def test_admin_page(self):
        response = self.client.get('/edit-page')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.content.decode('utf-8'), 'Админка')

    def test_add_article(self):
        response = self.client.post('/edit-page', {'name': 'user1', 'text': 'user1text1'})
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.content.decode('utf-8'), 'user1')

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.content.decode('utf-8'), 'user1')

    
