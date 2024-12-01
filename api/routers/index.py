from . import user, feedback, restaurant_staff, menu_items, order, payment, promotions


def load_routes(app):
    app.include_router(user.router)
    app.include_router(feedback.router)
    app.include_router(restaurant_staff.router)
    app.include_router(menu_items.router)
    app.include_router(order.router)
    app.include_router(payment.router)
    app.include_router(promotions.router)