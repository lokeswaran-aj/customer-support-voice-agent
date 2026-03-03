import uuid
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shared.db.models import Order, OrderScenario, OrderStatus, Refund


async def get_order_by_id_with_restaurant_and_items(
    session: AsyncSession, order_id: uuid.UUID
) -> Order | None:
    result = await session.execute(
        select(Order)
        .options(selectinload(Order.restaurant), selectinload(Order.items))
        .where(Order.id == order_id)
    )
    return result.scalar_one_or_none()


async def get_order_by_order_number_with_restaurant_and_items(
    session: AsyncSession, order_number: str
) -> Order | None:
    result = await session.execute(
        select(Order)
        .options(selectinload(Order.restaurant), selectinload(Order.items))
        .where(Order.order_number == order_number)
    )
    return result.scalar_one_or_none()


async def get_orders_by_scenario(
    session: AsyncSession, scenario: OrderScenario
) -> list[Order]:
    result = await session.execute(
        select(Order)
        .options(selectinload(Order.restaurant), selectinload(Order.items))
        .where(Order.scenario == scenario)
    )
    return result.scalars().all()


async def create_refund(
    session: AsyncSession, order_id: uuid.UUID, reason: str, amount: float
) -> Refund:
    refund = Refund(order_id=order_id, reason=reason, amount=amount)
    session.add(refund)
    await session.execute(
        update(Order)
        .where(Order.id == order_id)
        .values(status=OrderStatus.REFUND_REQUESTED)
    )
    await session.commit()
    return refund


async def update_order_status(
    session: AsyncSession,
    order_id: uuid.UUID,
    new_status: OrderStatus,
) -> None:
    await session.execute(
        update(Order).where(Order.id == order_id).values(status=new_status)
    )
    await session.commit()
