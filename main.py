import random
import string
import time
import pika
import threading
import argparse

from producer import producer
from sender import sender



def progress_monitor(sent_counts, failed_counts):
    start_time = time.time()
    while True:
        total_sent = sum(sent_counts)
        total_failed = sum(failed_counts)
        print(f"Messages sent: {total_sent}, Messages failed: {total_failed}")
        elapsed_time = time.time() - start_time
        if elapsed_time > 0 and total_sent + total_failed > 0:
            average_time_per_message = elapsed_time / (total_sent + total_failed)
            print(f"Messages sent: {total_sent}, Messages failed: {total_failed}, Average time per message: {average_time_per_message:.2f} seconds")
        
        if total_sent + total_failed >= num_senders * num_messages:
            # All messages have been processed
            break

        time.sleep(1)  # Update every 5 seconds (configurable)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_senders", type=int, default=1, help="Number of sender instances")
    parser.add_argument("--num_messages", type=int, default=1000, help="Number of SMS messages to generate")
    args = parser.parse_args()

    num_senders = args.num_senders
    num_messages = args.num_messages

    sent_counts = [0] * num_senders
    failed_counts = [0] * num_senders

    producer_thread = threading.Thread(target=producer, args=(num_messages,))
    producer_thread.start()

    sender_threads = []
    for i in range(num_senders):
        sender_thread = threading.Thread(target=sender, args=(i, num_messages, failed_counts, sent_counts))
        sender_threads.append(sender_thread)
        sender_thread.start()

    monitor_thread = threading.Thread(target=progress_monitor, args=(sent_counts, failed_counts))
    monitor_thread.start()

    producer_thread.join()
    for sender_thread in sender_threads:
        sender_thread.join()
    monitor_thread.join()
