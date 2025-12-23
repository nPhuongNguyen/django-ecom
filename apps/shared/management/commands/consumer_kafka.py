from django.core.management.base import BaseCommand

from ....config.kafka_config import KafkaConsumerWorker


class Command(BaseCommand):
    help = "Consume O2M Smartlink API log from Kafka"

    def handle(self, *args, **options):
        consumer = KafkaConsumerWorker()

        def process(key, value):
            print(key, value)

        self.stdout.write(self.style.SUCCESS("Kafka consumer started"))
        consumer.run(process)
