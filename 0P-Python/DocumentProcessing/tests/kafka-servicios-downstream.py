from confluent_kafka import Consumer, KafkaException,KafkaError

consumer = Consumer({
    #'bootstrap.servers': 'localhost:9092',
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'grupo-v1',
    'auto.offset.reset': 'earliest'
})



def main():
    topic:str='dato-comprimidos-v1'
    consumer.subscribe([topic])
    try:
        while True:
            msg = consumer.poll(timeout=5.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())


            print("Headers:", msg.headers())  # Devuelve lista de tuplas
            value = msg.value().decode('utf-8')
            #value = msg.value()
            print(f"Mensaje recibido: {value}")
    except Exception as e:
        print(f'Exception<{type(e).__name__}>, detail {e}')
    except KeyboardInterrupt:
        print('KeyboardInterrupt, peticion de finalizacion.')




if __name__ == '__main__':
    main()

## python3 tests/confluent-kafka/consumer.py
## bash activate.sh --python tests/confluent-kafka/consumer.py
