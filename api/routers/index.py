from . import user, feedback, restaurant_staff, menu_items, order, payment, promotions, customer_support, engagement_campaign


def load_routes(app):
    app.include_router(user.router)
    app.include_router(feedback.router)
    app.include_router(restaurant_staff.router)
    app.include_router(menu_items.router)
    app.include_router(order.router)
    app.include_router(payment.router)
    app.include_router(promotions.router)
    app.include_router(customer_support.router)
    app.include_router(engagement_campaign.router)