from django import template
#from AEBase.models.Dataset import Dataset
from django.utils.html import format_html
from django.urls import reverse
import math as math

register = template.Library()


# @register.simple_tag(takes_context=True)
# def dataset_select_tag(context, enabled=False):
#     if not context['request'].user.is_authenticated:
#         return ''
#     request = context['request']
#     datasets = Dataset.get_viewable_datasets(request)
#     if len(datasets) == 0:
#         return ''
#     dataset_id = Dataset.get_dataset_selection(request)
#     html = "<select name='DatasetSelect' id='DatasetSelect' "
#     if not enabled:
#         html += "disabled>"
#     else:
#         html += ">"
#     for a_dataset in datasets:
#         if a_dataset.id == dataset_id:
#             is_selected = 'selected'
#         else:
#             is_selected = ''
#         html += "<option value='" + str(a_dataset.id) + "' " + is_selected + ">" + str(a_dataset.subclass()) \
#                 + "</option>"
#     html += "</select>"
#     return html


# base.html block for username/groups/logout
@register.simple_tag(takes_context=True)
def user_block(context):
    if not context['request'].user.is_authenticated:
        return ''
    html = '<span class="hawthorne-blue fa fa-user fa-lg"></span> $USERNAME$ &nbsp;&nbsp;<a href="/accounts/logout">'
    html += '<i class="fa fa-sign-out"></i>logout</a><br/><span>Roles:&nbsp;$USER_ROLES$</span></br>'
    html = html.replace('$USERNAME$', context['request'].user.username)
    roles = str(list(context['request'].user.groups.values_list('name', flat=True)))
    roles = roles.replace(' ', '&nbsp;').replace("[", "").replace("]", "").replace("'", "")
    if roles == '':
        roles = 'None'
    html = html.replace('$USER_ROLES$', roles)
    return html


# this simple template tag is used to implement the Python statements
# RedisMetaData[dataset.id,'db'] and RedisMetaData[dataset.id,'l['last_loaded'] in the template as:
# <td>{% get_item2keys RedisMetaData dataset.id 'db' %}</td>
# <td>{% get_item2keys RedisMetaData dataset.id 'lastLoaded' %}</td>
# The tag can be used for other double dictionary lookups and probably extended to handle single/triple lookups.
# Note, this is only needed because one of the indexes is itself a variable.
@register.simple_tag
def get_item2keys(dictionary, first_key, second_key):
    if first_key in dictionary.keys():
        return dictionary[first_key][str(second_key)]
    first_key = str(first_key)
    if first_key in dictionary.keys():
        return dictionary[first_key][str(second_key)]
    return ''


@register.simple_tag(takes_context=True)
def hostname(context):
    return context['request'].get_host().split(':')[0]


@register.simple_tag
def group_tag_edit_link(url, object_id, tag_list):
    html = '<a class="tag_edit" data-id="' + reverse(url, kwargs={'pk': object_id}) + '" href="#">$VALUE$</a>'
    if tag_list == '':
        html = html.replace('$VALUE$', '<span class="hawthorne-red">no tags</span>')
    else:
        html = html.replace('$VALUE$', tag_list)
    return format_html(html)


@register.simple_tag
def check_mark(value):
    if value:
        return '<span class="hawthorne-blue">✔</span>'
    else:
        return '<span class="hawthorne-red">✘</span>'


@register.simple_tag
def format_to_digits(value, digits):
    return round(value, digits - math.ceil(math.log10(value)))
