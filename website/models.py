from django.db import models
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='authors', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    # def save (self,*args, **kwargs):
    #     if not self.slug:
    #         base_slug = slugify(self.name)
    #         self.name = base_slug
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Categories"
    

class Blog(models.Model):
    STATUS = {
        ('0', 'DRAFT'),
        ('1', 'PUBLISH')
    }

    SECTION = {
        ('Recent', 'Recent'),
        ('Popular', 'Popular'),
        ('Trending', 'Trending')
    }

    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='blogs', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    content = models.TextField() 
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE, default='Samuel Arhin')
    blog_slug = models.SlugField(max_length=255, unique=True, null=True, db_index=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=1, default=0)
    section = models.CharField(choices=SECTION, max_length=100)
    main_post = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} -- {self.category}"
    

class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    post = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    blog_id= models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website=models.URLField(blank=True, null=True)
    comment = models.TextField()
    date = models.DateField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies' )

    def save(self, *args, **kwargs):
        if self.post:
            self.blog_id = self.post.id
        super().save(*args, **kwargs)

        def __str__(self):
            return self.name