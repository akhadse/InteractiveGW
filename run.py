from app import create_app
import logging
import sys

app = create_app()

logging.basicConfig(filename='/home/akshay/logs/flask_app.log', level=logging.INFO, format='%(asctime)s %(message)s')

class LoggerWriter:
    def __init__(self, level):
        self.level = level

    def write(self, message):
        if message.strip() != "":  # Ignore empty messages
            self.level(message)

    def flush(self):
        pass  # This is required for the stream interface but can be a no-op

# Redirect stdout and stderr
sys.stdout = LoggerWriter(app.logger.info)
sys.stderr = LoggerWriter(app.logger.error)


if __name__=='__main__':
    #app.run(host="0.0.0.0", port=5000, debug=True)
    #app.run(debug=True)
    app.run()

