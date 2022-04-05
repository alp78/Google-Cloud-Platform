from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

project_id = 'vaulted-gate-343007'
topic_id = 'test-topic'
subscription_id = 'test-topic-sub'
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message.message_id}:\n{message}\n.")
    message.ack()
    print(f'Acknowledged with ack_id: {message.ack_id}')
    
    
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
