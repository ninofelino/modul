# -*- coding: utf-8 -*-
{
    'name': "felino",

    'summary': """
        Aplikasi konversi Data Lama Ke ODDO dalam rangka cutoff aplikasi
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Nuansa Baru Indonesia",
    'website': "https://www.facebook.com/ninofelino.felino",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/gatewaytmp.xml',
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],'application':True,
    
}