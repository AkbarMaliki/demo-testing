# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

{
    "name": "login_theme",
    "description": """hit_backlogin_themend_theme""",
    "summary": "Custom style based on code_backend_theme theme",
    "category": "Themes/Backend",
    "version": "0.1",
    'author': 'Malik',
    'company': 'Malik',
    'maintainer': 'Malik',
    'website': "",
    "depends": ['base', 'web', 'mail', 'code_backend_theme','get'],
    "data": [
        # 'views/base_setup.xml',
        # 'views/dakupentas.xml',
        'views/kasir.xml',
        'views/register.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'login_theme/static/src/scss/login.scss',
        ],
    },
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
