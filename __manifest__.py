# -*- coding: utf-8 -*-
{
    'name': "Base geolocalize extender",

    'summary': """
        Extending base_geolocalize""",

    'description': """
        Extending geocoder with reverse functionality
    """,

    'author': "Polimex Team",
    'website': "https://polimex.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base_geolocalize'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_company.xml',
    ],
    # only loaded in demonstration mode

}
