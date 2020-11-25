import json
import pika
import time
import threading

from flask import current_app
from listenbrainz.webserver.views.api_tools import LISTEN_TYPE_PLAYING_NOW, LISTEN_TYPE_IMPORT

EVENT_NAME = "playlist_updates"


class PlaylistEditsDispatcher(threading.Thread):

    def __init__(self, app, socket_io):
        threading.Thread.__init__(self)
        self.app = app
        self.socket_io = socket_io

    def send_playlist(self, playlist, room):
        self.socket_io.emit(EVENT_NAME, json.dumps(playlist), room=room)

    def callback_listen(self, channel, method, properties, body):
        listens = json.loads(body)
        self.send_playlist(listens, LISTEN_TYPE_IMPORT)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        with self.app.app_context():
            while True:
                current_app.logger.info("Starting PlaylistEditsDispatcher...")
                try:
                    while True:
                        pass
                except KeyboardInterrupt:
                    current_app.logger.error("Keyboard interrupt!")
                    break
                except Exception as e:
                    current_app.logger.error("Error in PlaylistEditsDispatcher: %s", str(e), exc_info=True)
                    time.sleep(3)
