broker_url = 'pyamqp://'
result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Moscow'

task_routes = {'run.check_values': 'low-priority',
               'run.calculate_results': 'high-priority',
               }
