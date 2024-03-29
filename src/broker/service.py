import json
import aio_pika
from src.settings.settings import settings


async def send_message_to_broker(email: str) -> dict:
    connection = await aio_pika.connect_robust(url=settings.broker_settings.broker_full_url)
    async with connection:
        routing_key = "email_register_queue"

        channel = await connection.channel()
        await channel.declare_queue("email_register_queue")

        await channel.default_exchange.publish(aio_pika.Message(body=email.encode()),
                                               routing_key=routing_key)


async def send_reset_code_to_broker(data: dict):
    connection = await aio_pika.connect_robust(url=settings.broker_settings.broker_full_url)
    async with connection:
        routing_key = "change_password_codes"

        channel = await connection.channel()
        await channel.declare_queue("change_password_codes")
        send_data = json.dumps(data)
        await channel.default_exchange.publish(aio_pika.Message(body=send_data.encode()),
                                               routing_key=routing_key)
