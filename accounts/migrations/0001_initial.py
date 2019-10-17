# Generated by Django 2.0.5 on 2018-09-19 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(max_length=150)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='postimages')),
            ],
        ),
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('seler', 'Seler'), ('normal', 'Normal')], default='Normal', max_length=7)),
                ('last_name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='usersImages')),
                ('address', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('offer', models.CharField(choices=[('selling', 'Selling'), ('Buying', 'Buying')], default='selling', max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('hide', 'Hide'), ('publish', 'Publish')], default='publish', max_length=10)),
                ('exchange', models.CharField(choices=[('accept', 'Accept'), ('refuse', 'Refuse')], default='refuse', max_length=20)),
                ('negotiation', models.CharField(choices=[('accept', 'Accept'), ('refuse', 'Refuse')], default='accept', max_length=20)),
                ('price', models.DecimalField(decimal_places=5, max_digits=15)),
                ('wilaya', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True)),
                ('phoneStatus', models.CharField(choices=[('4/10', '4/10'), ('5/10', '5/10'), ('6/10', '6/10'), ('7/10', '7/10'), ('8/10', '8/10'), ('9/10', '9/10'), ('10/10', '10/10')], default='10', max_length=5)),
                ('coverImg', models.ImageField(blank=True, null=True, upload_to='postimages')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='accounts.userPosts'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postImage', to='accounts.userPosts'),
        ),
    ]