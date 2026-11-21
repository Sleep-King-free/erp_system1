"""测试数据初始化脚本。

在 server 目录下执行：
    python -m app.db.seed_data

依赖：
    pip install passlib[bcrypt]

插入内容：
    1. 2 个测试账号：admin/admin123（ADMIN）、sales1/123456（SALES）
    2. 3 个假客户，均绑定在 sales1 名下
    3. 3 条假聊天记录，关联到第一个客户
"""
from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import select

from app.db.session import Base, SessionLocal, engine
from app.models import ChatRecord, Customer, User

# 密码哈希上下文（与后续登录校验保持一致）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed() -> None:
    # 确保表已创建（依赖 models 已在导入时注册到 Base.metadata）
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 防重复：已有用户数据则跳过
        if db.scalar(select(User).limit(1)) is not None:
            print("数据库已存在用户数据，跳过初始化（如需重插请先清空相关表）。")
            return

        # 1. 测试账号
        admin = User(
            username="admin",
            password_hash=pwd_context.hash("admin123"),
            role="ADMIN",
        )
        sales1 = User(
            username="sales1",
            password_hash=pwd_context.hash("123456"),
            role="SALES",
        )
        db.add_all([admin, sales1])
        db.flush()  # 先落库以获取自增 id

        # 2. 假客户，均归属 sales1
        customers = [
            Customer(
                name="杭州云启科技有限公司",
                contact="王海",
                phone="13800138001",
                industry="软件",
                source="行业展会",
                owner_id=sales1.id,
            ),
            Customer(
                name="宁波港口物流集团",
                contact="陈晓",
                phone="13900139002",
                industry="物流",
                source="老客户转介绍",
                owner_id=sales1.id,
            ),
            Customer(
                name="苏州智造精密",
                contact="刘敏",
                phone="13700137003",
                industry="制造",
                source="官网咨询",
                owner_id=sales1.id,
            ),
        ]
        db.add_all(customers)
        db.flush()  # 获取客户 id

        # 3. 假聊天记录，关联第一个客户
        chats = [
            ChatRecord(
                customer_id=customers[0].id,
                content="我是王海，杭州云启科技的采购经理。我们最近在做数字化升级，想上一套CRM，"
                        "预算20万以内，先了解一下你们的实施周期和售后。",
                channel="微信",
                occurred_at=datetime.now(),
            ),
            ChatRecord(
                customer_id=customers[0].id,
                content="内部讨论后倾向尽快推进，最好下个月能上线，担心数据安全和对接难度，"
                        "希望安排一次演示。",
                channel="微信",
                occurred_at=datetime.now(),
            ),
            ChatRecord(
                customer_id=customers[0].id,
                content="请把报价和同行业案例发我邮箱，我们评估后再约时间详谈。",
                channel="电话",
                occurred_at=datetime.now(),
            ),
        ]
        db.add_all(chats)

        db.commit()
        print("测试数据插入完成：2 个账号、3 个客户、3 条聊天记录。")
        print("账号：admin/admin123（ADMIN）、sales1/123456（SALES）")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
