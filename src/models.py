from enum import Enum as pyEnum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    userfirstname: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    password: Mapped[str] = mapped_column(nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user_from: Mapped[User] = relationship("User", foreign_keys=[user_from_id])
    user_to: Mapped[User] = relationship("User", foreign_keys=[user_to_id])

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship()

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String())

    autor_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship()

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped[Post] = relationship()

class Type(pyEnum):
        VIDEO = 1
        FOTO = 2
        REELS = 3
        STORY = 4


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Type] = mapped_column(Enum(Type))
    url: Mapped[str] = mapped_column(String())
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped[Post] = relationship()