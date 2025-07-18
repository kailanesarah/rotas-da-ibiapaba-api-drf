# Generated by Django 5.2.1 on 2025-07-07 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_establishment_description_alter_location_complement'),
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp', models.CharField(blank=True, help_text='Número do WhatsApp com DDD, ex: (88) 9 11999999', max_length=20, null=True)),
                ('instagram', models.CharField(blank=True, help_text='Usuario do instagram Ex:@joao_silva', max_length=20, null=True)),
                ('facebook', models.CharField(blank=True, help_text='Usuario do facebook Ex:joao_silva', max_length=20, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='establishment',
            old_name='CNPJ',
            new_name='cnpj',
        ),
        migrations.RemoveField(
            model_name='establishment',
            name='whatsapp',
        ),
        migrations.AddField(
            model_name='establishment',
            name='photos',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='establishment_photo', to='photos.establishmentprofileimage'),
        ),
        migrations.AddField(
            model_name='establishment',
            name='pix_key',
            field=models.CharField(blank=True, help_text='Chave Pix do estabelecimento (e-mail, telefone, CPF/CNPJ ou aleatória)', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='establishment',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='establishment',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='establishment_location', to='accounts.location'),
        ),
        migrations.AlterField(
            model_name='location',
            name='number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='establishment',
            name='social_media',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='establishments_social_media', to='accounts.socialmedia'),
        ),
    ]
