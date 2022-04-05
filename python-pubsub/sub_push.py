from google.cloud import pubsub_v1

project_id = 'vaulted-gate-343007'
topic_id = 'test-topic'
subscription_id = 'sub-push'
endpoint = 'https://vaulted-gate-343007.uc.r.appspot.com/push-handler'
timeout = 5.0

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)

