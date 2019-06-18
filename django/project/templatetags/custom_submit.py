from django.contrib.admin.templatetags.admin_modify import submit_row
from django.template.loader import get_template
from django import template

# Override submit row template. This is needed because there's no block defined for this in change_form.html
# that can be overridden, so the submit_row template tag's template needs to be changed
t = get_template('admin/project/projectimport/submit_line.html')
register = template.Library()
register.inclusion_tag(t, takes_context=True)(submit_row)
