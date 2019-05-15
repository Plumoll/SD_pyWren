"""
magi tell
guillem frisach
"""

import pywren_ibm_cloud as pywren
import yaml
import pika
import random

#done but not tested
class callback_rabbit_leader:
    def __init__(self, id, max_messages):
        self.__max_messages = max_messages
        self.__numerao = []
        self.__num_messages = 0
    def __call__(self, ch, method, properties, body):
        self.__num_messages += 1
        self.__numerao.append(int(body.decode('UTF-8')))
        if self.__num_messages is self.__max_messages:
            id  = random.randint(0, len(self.__numerao)-1)
            self.__num_messages = 0
            self.__max_messages -= 1
            self.__numerao = []
            ch.stop_consuming()
            ch.basic_publish(exchange='sd', routing_key='', body=id)
    def getNumerao(self):
        return self.__numerao

#not finished __call__
class callback_rabbit_slave:
    def __init__(self, id, max_messages):
        self.__max_messages = max_messages
        self.__numerao = [f'({id})']
        self.__num_messages = 0
        self.__id = id
        self.__active = True
    def __call__(self, ch, method, properties, body):
        num = int(body.decode('UTF-8'))
        #id
        if self.__num_messages < self.__max_messages:
            if num < 0:
                if -num == self.__id:
                    message = random.randint(0, 100)
                    ch.basic_publish(exchange='sd', routing_key='', body=message)
                    self.__active = False
            #num
            else:
                self.__num_messages += 1
                self.__numerao.append(int(body.decode('UTF-8')))

                self.__max_messages -= 1
                ch.stop_consuming()
    def getNumerao(self):
        return self.__numerao

#we need to implement both callbacks and a private queue for leader
def my_map_function(id):
    #return x + 5
    queue_id = f'queue{id}3'
    url = 'amqp://xbjymxoa:jdlKHnEzsJ3woxT8wHGtox-8PI7kJXwW@caterpillar.rmq.cloudamqp.com/xbjymxoa'
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='sd', exchange_type='fanout')
    callback = callback_rabbit(id)
    #a different queue for each function
    channel.queue_declare(queue_id)
    channel.queue_bind(exchange='sd', queue=queue_id)
    if id is not 0:
        channel.basic_publish(exchange='sd', routing_key='', body=id)
    channel.basic_consume(callback, queue=queue_id, no_ack=True)
    #start receiving messages
    channel.start_consuming()

    #close rabbitmq's connection
    connection.close()
    return callback.getNumerao()

#we need to call two different functions, leader and slave
if __name__ == '__main__':
    #load config file
    with open('ibm_cloud_config', 'r') as config_file:
        res = yaml.safe_load(config_file)
    url = res['rabbitmq']['url']
    #iteration_data = [[0,url], [1,url], [2,url], [3, url], [4, url]]
    #iteration_data = [1, 2, 3, 4, 5, 6, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    iteration_data = [0,'fortnite', 'is', 'better', 'than', 'apex']
    pw = pywren.ibm_cf_executor()
    pw.map(my_map_function, iteration_data)
    print(pw.get_result())
