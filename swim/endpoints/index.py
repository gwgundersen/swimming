"""Render landing page."""

import datetime
from flask import Blueprint, render_template
from flask.ext.login import login_required
import pytz

from swim import db, models
from swim.config import config


index_blueprint = Blueprint('index',
                            __name__,
                            url_prefix=config.get('url', 'base'))


@index_blueprint.route('/', methods=['GET'])
@login_required
def render_index_page():
    """Render index page.
    """
    todo = db.session.query(models.Task)\
        .filter_by(status='todo')\
        .order_by(models.Task.rank)\
        .all()

    queued = db.session.query(models.Task)\
        .filter_by(status='queued')\
        .order_by(models.Task.rank)\
        .all()

    u = datetime.datetime.utcnow()
    u = u.replace(tzinfo=pytz.utc)
    current_time = u.astimezone(pytz.timezone("America/New_York")).date()

    done = db.session.query(models.Task)\
        .filter(models.Task.status == 'done')\
        .filter(models.Task.date_completed == current_time)\
        .order_by(models.Task.rank)\
        .all()

    actions = models.Task.update_actions()
    return render_template('index.html', todo=todo, queued=queued,
                           done=done, actions=actions)
