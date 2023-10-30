import pika
from utils import generate_random_message, generate_random_phone_number
def producer(num_messages=1000):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')
    channel.confirm_delivery()


    for _ in range(num_messages):
        message = generate_random_message()
        phone_number = generate_random_phone_number()
        sms_data = (phone_number, message)
        # channel.basic_publish(exchange='', routing_key='sms_queue', body=str(sms_data))
        channel.basic_publish(exchange='',
                                  routing_key='sms_queue',
                                  body=str(sms_data),
                                  properties=pika.BasicProperties(
                                      delivery_mode=2, 
                                  ),
                                  mandatory=True)
    
    connection.close()
