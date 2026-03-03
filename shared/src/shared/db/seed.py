import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from shared.db.engine import AsyncSessionLocal
from shared.db.models import Order, OrderItem, OrderScenario, OrderStatus, Restaurant


async def seed():
    async with AsyncSessionLocal() as session:
        existing = await session.execute(select(Restaurant).limit(1))
        if existing.scalar_one_or_none() is not None:
            print("Database already seeded. Skipping.")
            return

        now = datetime.now(timezone.utc)

        burger_joint = Restaurant(
            name="The Burger Joint",
            address="12 King Street, Downtown",
            phone="+1-555-010-1234",
        )
        pizza_palace = Restaurant(
            name="Pizza Palace",
            address="45 Oak Avenue, Midtown",
            phone="+1-555-020-5678",
        )
        sushi_spot = Restaurant(
            name="Sushi Spot",
            address="78 Elm Road, Uptown",
            phone="+1-555-030-9012",
        )

        session.add_all([burger_joint, pizza_palace, sushi_spot])
        await session.flush()

        delayed_order = Order(
            order_number="QB1001",
            restaurant_id=burger_joint.id,
            scenario=OrderScenario.DELAYED,
            status=OrderStatus.OUT_FOR_DELIVERY,
            total_amount=34.97,
            delivery_address="22 Maple Lane, Apt 4B",
            estimated_delivery_at=now - timedelta(minutes=45),
        )

        missing_items_order = Order(
            order_number="QB1002",
            restaurant_id=pizza_palace.id,
            scenario=OrderScenario.MISSING_ITEMS,
            status=OrderStatus.DELIVERED,
            total_amount=52.96,
            delivery_address="9 Birch Boulevard, Suite 2",
            estimated_delivery_at=now - timedelta(hours=1),
        )

        wrong_order = Order(
            order_number="QB1003",
            restaurant_id=sushi_spot.id,
            scenario=OrderScenario.WRONG_ORDER,
            status=OrderStatus.DELIVERED,
            total_amount=61.98,
            delivery_address="31 Cedar Close",
            estimated_delivery_at=now - timedelta(hours=2),
        )

        cancelled_order = Order(
            order_number="QB1004",
            restaurant_id=burger_joint.id,
            scenario=OrderScenario.CANCELLED_BY_RESTAURANT,
            status=OrderStatus.CANCELLED,
            total_amount=27.98,
            delivery_address="5 Pine Street, Floor 3",
            estimated_delivery_at=now + timedelta(minutes=30),
        )

        double_charged_order = Order(
            order_number="QB1005",
            restaurant_id=pizza_palace.id,
            scenario=OrderScenario.DOUBLE_CHARGED,
            status=OrderStatus.DELIVERED,
            total_amount=44.97,
            delivery_address="17 Walnut Way",
            estimated_delivery_at=now - timedelta(hours=3),
        )

        session.add_all(
            [
                delayed_order,
                missing_items_order,
                wrong_order,
                cancelled_order,
                double_charged_order,
            ]
        )
        await session.flush()

        items = [
            # Delayed order — burger meal
            OrderItem(order_id=delayed_order.id, item_name="Classic Cheeseburger", item_price=12.99, item_quantity=2),
            OrderItem(order_id=delayed_order.id, item_name="Loaded Fries", item_price=5.99, item_quantity=1),
            OrderItem(order_id=delayed_order.id, item_name="Chocolate Milkshake", item_price=3.00, item_quantity=1),

            # Missing items order — pizza meal, garlic bread and drink are missing
            OrderItem(order_id=missing_items_order.id, item_name="Pepperoni Pizza (Large)", item_price=18.99, item_quantity=1),
            OrderItem(order_id=missing_items_order.id, item_name="Margherita Pizza (Medium)", item_price=14.99, item_quantity=1),
            OrderItem(order_id=missing_items_order.id, item_name="Garlic Bread", item_price=5.99, item_quantity=2, is_missing=True),
            OrderItem(order_id=missing_items_order.id, item_name="Cola (2L)", item_price=3.00, item_quantity=1, is_missing=True),

            # Wrong order — sushi meal (completely wrong food delivered)
            OrderItem(order_id=wrong_order.id, item_name="Salmon Sashimi (12 pcs)", item_price=22.99, item_quantity=1),
            OrderItem(order_id=wrong_order.id, item_name="Dragon Roll", item_price=16.99, item_quantity=1),
            OrderItem(order_id=wrong_order.id, item_name="Miso Soup", item_price=4.50, item_quantity=2),
            OrderItem(order_id=wrong_order.id, item_name="Green Tea", item_price=2.75, item_quantity=2),

            # Cancelled order — burger meal (cancelled by restaurant after order placed)
            OrderItem(order_id=cancelled_order.id, item_name="BBQ Bacon Burger", item_price=13.99, item_quantity=1),
            OrderItem(order_id=cancelled_order.id, item_name="Onion Rings", item_price=4.99, item_quantity=1),
            OrderItem(order_id=cancelled_order.id, item_name="Lemonade", item_price=3.00, item_quantity=1),
            OrderItem(order_id=cancelled_order.id, item_name="Ice Cream Sundae", item_price=6.00, item_quantity=1),

            # Double charged order — pizza meal (charged twice for same order)
            OrderItem(order_id=double_charged_order.id, item_name="Hawaiian Pizza (Large)", item_price=17.99, item_quantity=1),
            OrderItem(order_id=double_charged_order.id, item_name="Caesar Salad", item_price=9.99, item_quantity=1),
            OrderItem(order_id=double_charged_order.id, item_name="Sparkling Water", item_price=2.49, item_quantity=2),
            OrderItem(order_id=double_charged_order.id, item_name="Tiramisu", item_price=7.01, item_quantity=1),
        ]

        session.add_all(items)
        await session.commit()

        print("✓ Restaurants seeded: 3")
        print("✓ Orders seeded: 5 (one per scenario)")
        print("✓ Order items seeded: 19")


if __name__ == "__main__":
    asyncio.run(seed())
