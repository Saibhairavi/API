# Generated by Django 3.2.9 on 2022-02-22 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('rollno', models.IntegerField()),
                ('marks', models.IntegerField()),
                ('gm', models.CharField(max_length=64)),
                ('gf', models.CharField(max_length=64)),
            ],
        ),
    ]
