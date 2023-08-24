# -*- coding: utf-8 -*-
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class JiraWebhook(http.Controller):
    @http.route("/jira_webhook", type="json", auth="public", methods=['POST'],
                csrf=False)
    def get_webhook_url(self, *args, **kwargs):
        _logger.info('received webhook data')
        try:
            data = json.loads(request.httprequest.data)
            _logger.info(data, "jira_data")
            return {'status': 'success'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
