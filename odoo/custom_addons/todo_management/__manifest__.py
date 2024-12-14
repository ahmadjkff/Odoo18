{
    'name': 'To-Do',
    'summary': 'To-Do management system.',
    'author': 'Ahmad Alfakori',
    'category': 'To-Do',  # Add a relevant category
    'version': '18.0.0.1.0',
    'license': 'LGPL-3',
    'depends': ['base', 'app_one', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'views/res_partner_view.xml',
        'reports/task_reports.xml',
    ],
    'assets':{
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
