import sys
sys.path.append(r'C:\Users\rocky\Desktop\Stuff 2.0\Learning\Python API Development\FastAPI')
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import Column , Integer , String , Boolean , ForeignKey

class Post(Base):
    __tablename__  = "posts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer , primary_key=True , nullable = False)
    title = Column(String , nullable = False)
    content = Column(String , nullable = False)
    published = Column(Boolean , default=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
    "users.id", ondelete="CASCADE"), nullable=False)

    #owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))