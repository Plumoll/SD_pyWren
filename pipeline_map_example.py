"""
magi tell
guillem frisach
"""

import pywren_ibm_cloud as pywren
import yaml
import pika

class callback_rabbit:
    def __init__(self):
        self.__numerao = []
    def __call__(self, ch, method, properties, body):
        self.__numerao.append(int(body.decode('UTF-8')))
        ch.stop_consuming()
    def getNumerao(self):
        return self.__numerao


def my_map_function(id, url):
    #return x + 5
    queue_id = f'queue{id}'
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    callback = callback_rabbit()
    #a different queue for each function
    channel.queue_declare(queue_id)

    #each queue has its own callback
    channel.basic_consume(callback, queue=queue_id, no_ack=True)
    #start receiving messages
    channel.start_consuming()

    #close rabbitmq's connection
    connection.close()
    return callback.getNumerao()

def my_map_function(id, url):
    

if __name__ == '__main__':
    #load config file
    with open('ibm_cloud_config', 'r') as config_file:
        res = yaml.safe_load(config_file)
    url = res['rabbitmq']['url']
    iteration_data = [[1,url], [2,url], [3, url], [4, url]]
    pw = pywren.ibm_cf_executor()
    pw.map(my_map_function, iteration_data)
    print(pw.get_result())
