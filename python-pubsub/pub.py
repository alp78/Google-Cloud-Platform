from google.cloud import pubsub_v1

project_id = 'vaulted-gate-343007'
topic_id = 'test-topic'

publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(project_id, topic_id)

# data must be bytestring
data = 'Hello World!'.encode("utf-8")

future = publisher.publish(topic_path, data)

# message ID
print(future.result())

