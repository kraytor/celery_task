from datetime import datetime
from operator import add, mul, truediv, pow

from celery import Celery
from flask import abort, jsonify, request, make_response

from app import app, db, models


OPERATOR_DICT = {
    "add": add,
    "mul": mul,
    "div": truediv,
    "pow": pow
}


celery_ = Celery(__file__.split(".")[0])
celery_.config_from_object("celeryconfig")


def save_to_db(func_key, json_response, result):
    log = models.Log(ip=request.remote_addr,
                     function=func_key,
                     in_data=str(json_response),
                     result=result)

    db.session.add(log)
    db.session.commit()


@celery_.task
def check_values(json_response):
    if not json_response or len(json_response) != 2 or not all(isinstance(el, int) for el in json_response.values()):
        abort(400)


@celery_.task
def calculate_result(func_key, json_response):
    v1, v2 = json_response.values()
    func = OPERATOR_DICT[func_key]

    return func(v1, v2)

@celery_.task
def get_statistic():
    now_ = datetime.strftime(datetime.now(), "%Y-%m-%d")
    result = db.session.query(models.Log.function, db.func.count(models.Log.function)).filter(
            models.Log.date.like("%{}%".format(now_))).group_by(models.Log.function).all()

    result = {el[0]: el[1] for el in result}
    return result


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/add', methods=['POST'])
def my_add():
    check_values(request.json)

    func_key = 'add'
    result = calculate_result.delay(func_key, request.json).wait()
    save_to_db(func_key, request.json, result)

    return jsonify({"result": result}), 201


@app.route('/api/mul', methods=['POST'])
def my_mul():
    check_values(request.json)

    func_key = 'mul'
    result = calculate_result.delay(func_key, request.json).wait()
    save_to_db(func_key, request.json, result)

    return jsonify({"result": result}), 201


@app.route('/api/div', methods=['POST'])
def my_div():
    check_values(request.json)

    func_key = 'div'
    result = calculate_result.delay(func_key, request.json).wait()
    save_to_db(func_key, request.json, result)

    return jsonify({"result": result}), 201


@app.route('/api/pow', methods=['POST'])
def my_pow():
    check_values(request.json)

    func_key = 'pow'
    result = calculate_result.delay(func_key, request.json).wait()
    save_to_db(func_key, request.json, result)

    return jsonify({"result": result}), 201


@app.route('/api/report')
def report():
    report = get_statistic.delay().wait()
    return jsonify({"result": report}), 201


if __name__ == '__main__':
    app.run(debug=True)
