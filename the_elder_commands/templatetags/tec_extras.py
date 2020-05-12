from django import template

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key, "")


@register.filter
def get_chosen_amount(service, item):
    form_id = item.get("formId")
    amount = service.chosen.get(form_id, "")
    return amount
