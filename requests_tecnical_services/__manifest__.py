{
    "name": "technical_service_request",
    "summary": """
        Request Tecnical Services""",
    "author": "Jmacea",
    "sequence": -100,
    "version": "17.0",
    "depends": ["base", "web", "point_of_sale"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "reports/paperformat.xml",
        "views/report_header_footer.xml",
        "views/report_technical_service_request.xml",
        "views/technical_service_request_views.xml",
        "views/request_form_templates.xml",
        "reports/action_report.xml",
        "data/email_template.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "requests_tecnical_services/static/src/js/request_form.js",
        ],
        'point_of_sale._assets_pos': [
            'requests_tecnical_services/static/src/post/components/button_request.js',
            'requests_tecnical_services/static/src/post/components/button_request.xml',
        ],
    },
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
