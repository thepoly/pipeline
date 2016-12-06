import asyncio
import asyncio_redis
import json
import uuid
import websockets

redis = None
sockets = dict()
send_queue = asyncio.Queue()


@asyncio.coroutine
def initialize():
    global redis
    redis = yield from asyncio_redis.Pool.create(host='localhost', poolsize=10, db=1)
    yield from redis.delete(['clients', 'documents'])


@asyncio.coroutine
def handler(websocket, path):
    client_id = str(uuid.uuid4())
    sockets[client_id] = websocket
    yield from redis.sadd('clients', [client_id])

    print('client connected')
    data = {'id': client_id, 'method': 'new'}
    yield from send_queue.put((client_id, json.dumps(data)))

    while True:
        message = yield from websocket.recv()
        if message is None:
            break
        yield from consumer(client_id, message)


@asyncio.coroutine
def consumer(client_id, msg):
    data = json.loads(msg)

    if data['method'] == 'edit_delta':
        print('edit_delta')
        document_id = data['document_id']
        delta = data['delta']
        data = {'method': 'edit_delta', 'editor_id': client_id, 'delta': delta}

        yield from redis.rpush('document:deltas:{}'.format(document_id), [json.dumps(delta)])

        c_set = yield from redis.smembers('document_clients:{}'.format(document_id))
        for c_id in c_set:
            client_id = yield from c_id
            yield from send_queue.put((client_id, json.dumps(data)))

    elif data['method'] == 'sync':
        print('sync')
        document_id = data['document_id']

        # set document value and deleting deltas atomically
        transaction = yield from redis.multi()
        yield from transaction.set('document:{}'.format(document_id), data['value'])
        yield from transaction.delete(['document:deltas:{}'.format(document_id)])
        yield from transaction.exec()

        data = {'method': 'sync', 'editor_id': client_id, 'value': data['value']}

        c_set = yield from redis.smembers('document_clients:{}'.format(document_id))
        for c_id in c_set:
            client_id = yield from c_id
            yield from send_queue.put((client_id, json.dumps(data)))

    elif data['method'] == 'create_document':
        print('create_document')
        document_id = str(uuid.uuid4())
        data = {'method': 'create_document', 'document_id': document_id}
        yield from redis.sadd('documents', [document_id])
        yield from redis.sadd('document_clients:{}'.format(document_id), [client_id])

        yield from send_queue.put((client_id, json.dumps(data)))

    elif data['method'] == 'join_document':
        print('join_document')
        document_id = data['document_id']
        yield from redis.sadd('document_clients:{}'.format(document_id), [client_id])

        document_value = yield from redis.get('document:{}'.format(document_id))
        document_deltas = yield from redis.lrange_aslist('document:deltas:{}'.format(document_id))
        data = {'method': 'join_document', 'document_value': document_value, 'document_deltas': [json.loads(x) for x in document_deltas]}
        yield from send_queue.put((client_id, json.dumps(data)))


@asyncio.coroutine
def producer():
    while True:
        data = yield from send_queue.get()
        client_id = data[0]
        if client_id in sockets:
            socket = sockets[client_id]
            if socket.open:
                yield from socket.send(data[1])
                print('sent {}'.format(json.loads(data[1])['method']))


asyncio.get_event_loop().run_until_complete(initialize())
start_server = websockets.serve(handler, '0.0.0.0', 8003)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(producer())
print('Server started.')
asyncio.get_event_loop().run_forever()
