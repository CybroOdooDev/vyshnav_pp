# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Gokul P I (odoo@cybrosys.com)
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
################################################################################
import json
import requests
from requests.auth import HTTPBasicAuth
from odoo import api, fields, models, _

HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}


class ProjectProject(models.Model):
    """ This class is inherited for adding some extra field and override the 
    create function
    Methods:
        create():
            extends create() to export project to Jira"""
    _inherit = 'project.project'

    project_id_jira = fields.Integer(string='Jira Project ID',
                                     help='Corresponding project id of Jira')
    jira_project_key = fields.Char(string='Jira Project Key',
                                   help='Corresponding project key of Jira')

    @api.model_create_multi
    def create(self, vals_list):
        """ Overrides create method of project to export project to Jira """
        self = self.with_context(mail_create_nosubscribe=True)
        projects = super().create(vals_list)
        jira_connection = self.env['ir.config_parameter'].sudo().get_param(
            'odoo_jira_connector.connection')
        if jira_connection:
            jira_url = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_jira_connector.url', '')
            user = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_jira_connector.user_id_jira', False)
            password = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_jira_connector.api_token', False)
            auth = HTTPBasicAuth(user, password)
            project_headers = {'Accept': 'application/json'}
            response = requests.request(
                'GET', jira_url + 'rest/api/2/project',
                headers=project_headers, auth=auth)
            projects_json = json.dumps(json.loads(response.text), sort_keys=True,
                                  indent=4, separators=(',', ': '))
            project_json = json.loads(projects_json)
            name_list = [project['name'] for project in project_json]
            key = projects.name.upper()
            project_key = key[:3] + '1' + key[-3:]
            project_keys = project_key.replace(' ', '')
            auth = HTTPBasicAuth(user, password)
            project_payload = {
                'name': projects.name, 'key': project_keys,
                'templateKey': 'com.pyxis.greenhopper.jira:gh-simplified'
                               '-kanban-classic'
            }
            if projects.name not in name_list:
                response = requests.request(
                    'POST', jira_url + 'rest/simplified/latest/project',
                    data=json.dumps(project_payload),
                    headers=HEADERS, auth=auth)
                data = response.json()
                projects.write({'project_id_jira': data['projectId'],
                                'jira_project_key': data['projectKey']})
                self.env['ir.config_parameter'].sudo().set_param(
                    'import_project_count', int(
                        self.env['ir.config_parameter'].sudo().get_param(
                            'import_project_count')) + 1)
        return projects


class ProjectTask(models.Model):
    """ This class is inherited for adding some extra field and override the
        create function
        Methods:
            create():
                extends create() to export tasks to Jira
            unlink():
                to delete a task in Jira when we delete the task in Odoo """
    _inherit = 'project.task'

    task_id_jira = fields.Char(string='Jira Task ID', help='Task id of Jira')
    jira_task_key = fields.Char(string='Jira Task Key',
                                help='Task key of Jira')

    @api.model
    def create(self, vals_list):
        """ Override the create method of tasks to export tasks to Jira """
        res = super(ProjectTask, self).create(vals_list)
        jira_connection = self.env['ir.config_parameter'].sudo().get_param(
            'odoo_jira_connector.connection')
        if jira_connection:
            jira_url = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_jira_connector.url', '')
            user = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_jira_connector.user_id_jira')
            password = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_jira_connector.api_token')
            query = {'jql': 'project = %s' % res.project_id.jira_project_key}
            requests.get(jira_url + 'rest/api/3/search', headers=HEADERS,
                         params=query, auth=(user, password))
            if not res.task_id_jira:
                payload = json.dumps({
                    'fields': {
                        'project': {'key': res.project_id.jira_project_key},
                        'summary': res.name,
                        'description': res.description,
                        'issuetype': {'name': 'Task'}
                    }
                })
                response = requests.post(
                    jira_url + '/rest/api/2/issue', headers=HEADERS,
                    data=payload, auth=(user, password))
                data = response.json()
                res.task_id_jira = str(data['key'])
                self.env['ir.config_parameter'].sudo().set_param(
                    'export_task_count', int(
                        self.env['ir.config_parameter'].sudo().get_param(
                            'export_task_count')) + 1)
        return res

    def unlink(self):
        """ Overrides the unlink method of task to delete a task in Jira when
        we delete the task in Odoo """
        for task in self:
            if task.stage_id and task.stage_id.fold:
                raise Warning(_('You cannot delete a task in a folded stage.'))
            jira_connection = self.env['ir.config_parameter'].sudo().get_param(
                'odoo_jira_connector.connection')
            if jira_connection:
                jira_url = self.env['ir.config_parameter'].sudo().get_param(
                    'odoo_jira_connector.url', '')
                user = self.env['ir.config_parameter'].sudo().get_param(
                    'odoo_jira_connector.user_id_jira')
                password = self.env['ir.config_parameter'].sudo().get_param(
                    'odoo_jira_connector.api_token')
                if task.task_id_jira:
                    requests.delete(
                        jira_url + '/rest/api/3/issue/' + task.task_id_jira,
                        headers=HEADERS, auth=(user, password))
        return super(ProjectTask, self).unlink()
