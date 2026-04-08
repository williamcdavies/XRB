import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api_groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileAccessControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(help_text='Relative path within the group directory, e.g. "reports/q1.csv" or "secret-data".', max_length=1024)),
                ('allowed_users', models.ManyToManyField(blank=True, related_name='file_access_grants', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_access_controls', to='auth.group')),
            ],
            options={
                'unique_together': {('group', 'path')},
            },
        ),
    ]
