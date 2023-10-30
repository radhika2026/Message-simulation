import pika
import time
import random

def sender(sender_id, num_messages, failed_counts, sent_counts):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')

    def callback(ch, method, properties, body):
        phone_number, message = eval(body)
        # Simulate message sending with random failures
        mean_processing_time = 2.0  # Example mean processing time in seconds
        error_rate = 0.05  # Example error rate (5%)
        
        time.sleep(random.uniform(mean_processing_time - 1, mean_processing_time + 1))
        if random.random() < error_rate:
            print(f"Sender {sender_id}: Message to {phone_number} failed: {message}")
            failed_counts[sender_id] += 1
        else:
            print(f"Sender {sender_id}: Message to {phone_number} sent: {message}")
            sent_counts[sender_id] += 1

    channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
