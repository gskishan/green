
import frappe
from erpnext.projects.doctype.project.project import Project
from frappe.utils import today

class CustomProject(Project):
    def copy_from_template(self):
        """
        Copy tasks from template
        """
        if self.project_template or self.custom_from_template and not frappe.db.get_all("Task", dict(project=self.name), limit=1):
			# has a template, and no loaded tasks, so lets create
            if not self.expected_start_date:
				# project starts today
                self.expected_start_date = today()

            proj_template = self.custom_from_template
            if self.project_template:
                proj_template = self.project_template
            template = frappe.get_doc("Project Template", proj_template)

            if not self.project_type:
                self.project_type = template.project_type

			# create tasks from template
            project_tasks = []
            tmp_task_details = []
            for task in template.tasks:
                template_task_details = frappe.get_doc("Task", task.task)
                tmp_task_details.append(template_task_details)
                task = self.create_task_from_template(template_task_details)
                project_tasks.append(task)

            self.dependency_mapping(tmp_task_details, project_tasks)