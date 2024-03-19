
{
    "name": "Custom Invoice Format Print",
    "summary": "Custom Invoice Format Print",
    "version": "14.0.1.0.1",
    "author": "Metamorphosis"", Joyanto",
    "website": "https://metamorphosis.com.bd",
    "category": "Tools",
    "depends": [
        "account", 'sale'
    ],
    "license": "LGPL-3",
    "data": [
        'views/invoice_reports.xml',
        'views/account_invoice_custom_report_template.xml',
        'views/invoice_duplicate_report.xml',
        'views/invoice_template_duplicate.xml',
    ],
    'sequence': 1,
    "installable": True,
    "auto_install": False,
    "application": True,
}