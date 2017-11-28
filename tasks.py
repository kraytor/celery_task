from operator import add, mul, truediv, pow

from celery import Celery


OPERATOR_DICT = {
    "add": add,
    "mul": mul,
    "div": truediv,
    "pow": pow
}


celery_ = Celery(app.name)
celery_.config_from_object("celeryconfig")


@celery_.task
def check_values(json_response):
    if not json_response or len(json_response) != 2 or not all(isinstance(el, int) for el in json_response.values()):
        abort(400)


@celery_.task
def calculate_result(func_key, json_response):
    v1, v2 = json_response.values()
    func = OPERATOR_DICT[func_key]
    return func(v1, v2)



# @app.task
# def add(x, y):
#     return x + y
#
#
# @app.task
# def mul(x, y):
#     return x * y
#
#
# @app.task
# def div(x, y):
#     return x / y
#
#
# @app.task
# def power(x, y):
#     return x ** y
