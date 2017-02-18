from . import main
from .. import db
import app.models as models

def LastFive():
    query = models.Games.query.order_by(models.Games.id.desc()).limit(5).all()
    return query
