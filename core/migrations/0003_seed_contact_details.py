from django.db import migrations

OLD_HERO_SUB = ('Strategy, Projects, Research & Funding consultancy for SMEs, '
                'NGOs and investors in Zimbabwe and the region.')
NEW_HERO_SUB = ('Strategy, Projects, Research & Funding consultancy for SMEs, '
                'NGOs and investors across Africa.')

CONTACT_DEFAULTS = {
    'contact_email': 'support@growthmastersolutions.com',
    'contact_email_secondary': 'growthmaster1@outlook.com',
    'phone': '0718 515 221 / 0775 222 468',
    'physical_address': ('Murewa Branch — Bokoto Mini Complex, Office Room FF6\n'
                         'Harare Branch — Suite C3A, Centre 171, Strathaven, Avondale West'),
}


def fill_contact_details(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    obj = SiteSettings.objects.filter(pk=1).first()
    if obj is None:
        return
    changed = []
    for field, value in CONTACT_DEFAULTS.items():
        if not getattr(obj, field):
            setattr(obj, field, value)
            changed.append(field)
    if obj.hero_subheading == OLD_HERO_SUB:
        obj.hero_subheading = NEW_HERO_SUB
        changed.append('hero_subheading')
    if changed:
        obj.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_sitesettings_contact_email_secondary_and_more'),
    ]

    operations = [
        migrations.RunPython(fill_contact_details, migrations.RunPython.noop),
    ]
