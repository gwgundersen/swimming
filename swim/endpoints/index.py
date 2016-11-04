"""Render landing page."""

import datetime
from flask import Blueprint, render_template, request
from flask.ext.login import login_required

from swim import db, models
from swim.config import config


index_blueprint = Blueprint('index',
                            __name__,
                            url_prefix=config.get('url', 'base'))


@login_required
@index_blueprint.route('/', methods=['GET'])
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

    current_time = datetime.datetime.utcnow()
    two_days_ago = current_time - datetime.timedelta(days=2)
    done = db.session.query(models.Task)\
        .filter(models.Task.status == 'done')\
        .filter(models.Task.date_completed > two_days_ago)\
        .order_by(models.Task.rank)\
        .all()

    actions = models.Task.update_actions()
    return render_template('index.html', todo=todo, queued=queued,
                           done=done, actions=actions)
