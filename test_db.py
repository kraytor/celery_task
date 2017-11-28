import random

from datetime import datetime
from operator import add, mul, truediv, pow

from app import db, models


OPERATOR_DICT = {
    "add": add,
    "mul": mul,
    "div": truediv,
    "pow": pow
}


models.Log.query.delete()

in_template = "'x':{}, 'y':{}"
list_of_logs = []

for _ in range(1000):
    op = random.choice(list(OPERATOR_DICT))
    x = random.randint(1, 100)
    y = random.randint(1, 100)

    log = models.Log(ip='172.1.1.1',
                     function=op,
                     in_data=in_template.format(x, y),
                     result=OPERATOR_DICT[op](x, y))

    list_of_logs.append(log)

db.session.add_all(list_of_logs)

db.session.commit()


now_ = datetime.strftime(datetime.now(), "%Y-%m-%d")

logs = db.session.query(models.Log.function, db.func.count(models.Log.function)).filter(models.Log.date.like("%{}%".format(now_))).group_by(models.Log.function).all()

print(logs)
