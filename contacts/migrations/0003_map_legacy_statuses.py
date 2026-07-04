from django.db import migrations


def map_legacy_statuses(apps, schema_editor):
    Enquiry = apps.get_model('contacts', 'Enquiry')
    Enquiry.objects.filter(status='read').update(status='in_progress')
    Enquiry.objects.filter(status__in=['replied', 'archived']).update(status='resolved')


def reverse_statuses(apps, schema_editor):
    Enquiry = apps.get_model('contacts', 'Enquiry')
    Enquiry.objects.filter(status='in_progress').update(status='read')
    Enquiry.objects.filter(status='resolved').update(status='replied')


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_alter_enquiry_status'),
    ]

    operations = [
        migrations.RunPython(map_legacy_statuses, reverse_statuses),
    ]
