from . import user, feedback, restaurant_staff, menu_items, order, payment, promotions, customer_support, engagement_campaign, training
from ..dependencies.database import engine

def index():
    user.Base.metadata.create_all(engine)
    feedback.Base.metadata.create_all(engine)
    restaurant_staff.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    order.Base.metadata.create_all(engine)
    payment.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    customer_support.Base.metadata.create_all(engine)
    engagement_campaign.Base.metadata.create_all(engine)
    training.Base.metadata.create_all(engine)
