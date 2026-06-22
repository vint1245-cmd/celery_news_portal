from django import template


register = template.Library()


STOP_LIST =  [
    'моды',
    'барселона',
    'суд',
]


@register.filter()
def censor(text):
    if type(text) is str:
        for word in STOP_LIST:
            if word in text.casefold():
                text =text.replace(word[1:], "*" *(len(word)-1))
    return text