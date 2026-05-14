"""
Copyright 2026, Jesus Emanuel Luccioni
All rights reserved.

This file is part of devops for Open Container (in this case docker )

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

THIS SCRIPT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SCRIPT, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

@file kafka-servicios-downstream.py
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.3.
@date Jueves 14 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version    Brief
JEL            2026.04.14     0.0.3      Version Inicial no release
"""
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
