# Generated by Django 3.1.7 on 2021-03-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorei', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(db_column='user_id', primary_key=True, serialize=False)),
                ('first_name', models.TextField(db_column='first_name', max_length=10)),
                ('middle_name', models.TextField(blank=True, db_column='middle_name', max_length=10, null=True)),
                ('last_name', models.TextField(blank=True, db_column='last_name', max_length=10, null=True)),
                ('email_address', models.EmailField(db_column='email_address', max_length=40)),
                ('house_number', models.CharField(blank=True, db_column='house_number', max_length=10, null=True)),
                ('street_number', models.CharField(blank=True, db_column='street_number', max_length=10, null=True)),
                ('street_name', models.TextField(db_column='street_name', max_length=50)),
                ('city', models.TextField(db_column='city', max_length=50)),
                ('state', models.TextField(db_column='state', max_length=50)),
                ('postal_code', models.DecimalField(db_column='zipcode', decimal_places=0, max_digits=6)),
                ('password', models.CharField(db_column='password', max_length=256)),
            ],
        ),
    ]
