from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   rating = models.IntegerField(default=0)

   def update_rating(self):
       posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'),0))['pr']
       comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'),0))['cr']
       posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'),0))['pcr']

       print(posts_rating)
       print('------------------')
       print(comments_rating)
       print('------------------')
       print(posts_comments_rating)

       self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
       self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=100,unique= True)
    subscribers = models.ManyToManyField(User,blank=True,null=True, related_name='categories')

    def __str__(self):
        return self.category_name.title()
class Post(models.Model):
    article = 'AT'
    news = 'NW'
    PUBLICATION = [(article, 'Статья'),(news, 'Новости')]
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    publication = models.CharField(max_length=2, choices=PUBLICATION, default=article)
    time_of_posting = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        small_text = self.text[:123]+"..."
        return small_text

    def __str__(self):
        return f'{self.title}: {self.text[:40]}'

    def get_absolute_url(self):
        return f'/news/{self.id}' #reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

#class Subscribers(models.Model):
   # user = models.ForeignKey(User,on_delete=models.CASCADE)
   # category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text_of_comment = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

