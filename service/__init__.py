"""Flask application package."""

from flask import Flask

app = Flask(__name__)

from service import routes  # noqa: E402,F401
from service.common import log_handlers  # noqa: E402

log_handlers.init_logging(app, "gunicorn.error")
app.logger.info("SERVICERUNNING")