# Generated by Django 5.2 on 2025-05-25 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_alter_blog_section_alter_blog_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='section',
            field=models.CharField(choices=[('Popular', 'Popular'), ('Trending', 'Trending'), ('Recent', 'Recent')], max_length=100),
        ),
    ]
