# Generated by Django 2.0 on 2019-01-10 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(db_index=True, max_length=50, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('id', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='LocalArea',
            fields=[
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('id', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
                ('state_id', models.CharField(blank=True, max_length=4, null=True)),
            ],
            options={
                'db_table': 'localarea',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MemberType',
            fields=[
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('id', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=60, verbose_name='code')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'passwordresetcode',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bio', models.TextField(blank=True)),
                ('image', models.URLField(blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.CreateModel(
            name='SignupCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=60, verbose_name='code')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('ipaddr', models.GenericIPAddressField(default='0.0.0.0', verbose_name='ip address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'signupcode',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('name', models.CharField(blank=True, max_length=70, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False, unique=True)),
                ('country_id', models.CharField(blank=True, max_length=3, null=True)),
            ],
            options={
                'db_table': 'state',
            },
        ),
        migrations.CreateModel(
            name='UserDefaultMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibe_user.Member')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'userdefaultmember',
            },
        ),
        migrations.CreateModel(
            name='VibespotMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_member_admin', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('approval_date', models.DateTimeField(auto_now_add=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibe_user.Member')),
                ('member_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibe_user.MemberType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='member_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vibe_user.MemberType'),
        ),
        migrations.AddField(
            model_name='user',
            name='member_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vibe_user.MemberType'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('name', 'member_type')},
        ),
    ]
