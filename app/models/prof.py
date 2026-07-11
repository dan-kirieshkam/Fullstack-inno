# from app.database import Base
# from enum import Enum

# from sqlalchemy import Boolean, String, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship


# class Profile(Base):
#     __tablename__ = "profiles"

#     id: Mapped[int] = mapped_column(primary_key=True)

#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id"),
#         unique=True,
#     )

#     user: Mapped["User"] = relationship(
#         back_populates="profile",
#     )

#     name: Mapped[str] = mapped_column(String, nullable=True)

#     bursday: Mapped[str] = mapped_column(String, nullable=True) 

#     prev: Mapped[str] = mapped_column(String, nullable=True)