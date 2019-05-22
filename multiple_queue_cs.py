"""
magi tell
guillem frisach
"""
import pywren_ibm_cloud as pywren
import pika
import random
import json
import os

#done but not tested
class callback_rabbit_leader:
    def __init__(self, max_messages):
        self.__active_slaves = max_messages
        self.__numerao = []
        self.__num_messages = 0
    def __call__(self, ch, method, properties, body):
        self.__num_messages += 1
        self.__numerao.append(int(body.decode('UTF-8')))
        #num = int(body.decode('UTF-8'))
        #print(f'missatge callback leader: {num}')
        if self.__num_messages is self.__active_slaves:
            #print(f'numerao: {self.__numerao}')
            id = random.randint(0, len(self.__numerao)-1)
            id = -self.__numerao[id]
            self.__num_messages = 0
            self.__active_slaves -= 1
            self.__numerao = []
            ch.basic_publish(exchange='sd', routing_key='', body=str(id))
            if self.__active_slaves is 0:
                ch.stop_consuming()
    def getNumerao(self):
        return self.__numerao

#not finished __call__
class callback_rabbit_slave:
    def __init__(self, id):
        self.__numerao = [f'({id})']
        self.__num_messages = -1
        self.__id = id
        self.__active = True
    def __call__(self, ch, method, properties, body):
        num = int(body.decode('UTF-8'))
        #print(f'missatge callback slave: {num}')
        #id
        if self.__num_messages is -1:
            self.__num_messages = num
            ch.stop_consuming()

        elif num <= 0:
            num = -num
            if num == self.__id and self.__active is True:
                message = random.randint(1, 100)
                ch.basic_publish(exchange='sd', routing_key='', body=str(message))
                self.__active = False
        else:
            self.__numerao.append(int(body.decode('UTF-8')))
            ch.stop_consuming()

    def get_numerao(self):
        return self.__numerao
    def get_num_messages(self):
        return self.__num_messages
    def is_active(self):
        return self.__active

def my_function_leader(num_slaves):
    pywren_Conf =  json.loads(os.environ.get('PYWREN_CONFIG', ''))
    url = pywren_Conf['rabbitmq']['amqp_url']
    callback = callback_rabbit_leader(num_slaves)
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare('queue_leaderxxx3')
    channel.exchange_declare(exchange='sd', exchange_type='fanout')
    for id in range(0, num_slaves):
        queue_id = f'queue{id}xxx3'
        channel.queue_declare(queue_id)
        channel.queue_bind(exchange='sd', queue=queue_id)
    channel.basic_publish(exchange='sd', routing_key='', body=str(num_slaves))
    channel.basic_consume(callback, queue='queue_leaderxxx3', no_ack=True)
    channel.start_consuming()
    return callback.getNumerao()

def my_function_slave(id):
    queue_id = f'queue{id}xxx3'
    pywren_Conf =  json.loads(os.environ.get('PYWREN_CONFIG', ''))
    url = pywren_Conf['rabbitmq']['amqp_url']
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='sd', exchange_type='fanout')
    callback = callback_rabbit_slave(id)
    channel.queue_declare(queue_id)
    channel.queue_bind(exchange='sd', queue=queue_id)
    channel.basic_consume(callback, queue=queue_id, no_ack=True)
    channel.start_consuming()

    for _ in range(0, callback.get_num_messages()):
        #print(f'numero iteracio: {_}')
        if(callback.is_active()):
            channel.basic_publish(exchange='', routing_key='queue_leaderxxx3', body=str(id))
        channel.basic_consume(callback, queue=queue_id, no_ack=True)
        channel.start_consuming()

    return callback.get_numerao()


#we need to call two different functions, leader and slave
if __name__ == '__main__':
    #load config file
    pw = pywren.ibm_cf_executor(rabbitmq_monitor=True)
    pw.map(my_function_slave, range(3))
    pw1 = pywren.ibm_cf_executor(rabbitmq_monitor=True)
    pw1.call_async(my_function_leader, 3)
    print(pw.get_result())
