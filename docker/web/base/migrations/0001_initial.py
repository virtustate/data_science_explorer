# Generated by Django 3.1.1 on 2020-09-13 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('connection_type', models.CharField(choices=[('csv', 'csv'), ('Snowflake', 'Snowflake')], default='csv', max_length=20)),
                ('created', models.DateTimeField(null=True)),
            ],
        ),
    ]
