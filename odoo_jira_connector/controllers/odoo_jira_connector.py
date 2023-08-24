# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request


class JiraWebhook(http.Controller):
    @http.route("/jira_webhook", type="json", auth="public", methods=['POST'],
                csrf=False)
    def get_webhook_url(self, *args, **kwargs):
        print('received webhook data')
        try:
            data = json.loads(request.httprequest.data)
            print(data)
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
