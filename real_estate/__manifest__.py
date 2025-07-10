# -*- coding: utf-8 -*-
{
    'name': "real_estate",

    'summary': "A Simple Real Estate Module",

    'description': """
A Simple Real Estate Module
    """,

    'author': "MindSynthTechnogy@Avishek",
    'website': "https://www.mindsynthtech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'other',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/property_report_template.xml',
        'views/property_views.xml',
        'views/property_offer.xml',
        'views/property_type.xml',
        'views/property_tag.xml',
        'views/res_users_inherited_view.xml',
        'views/menu.xml',
    ],
'assets': {
    'web.assets_backend': [
        'real_estate/static/src/components/*/**.js',
        'real_estate/static/src/components/*/**.xml',
    ],
}
}