from sqlalchemy import create_engine, Column, VARCHAR, CHAR, BOOLEAN, BIGINT, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
import os

db_url = os.environ.get("DB_URL")
db_pass = os.environ.get("DB_Password")
engine = create_engine("mysql+mysqlconnector://root:{0}@{1}/mydb".format(db_pass, db_url))
Session = sessionmaker(bind=engine)

Base = declarative_base()

association_table = Table("Users_has_Recipient", Base.metadata,
                          Column("Users_uuid", CHAR(36), ForeignKey("Users.uuid")),
                            Column("Recipient_uuid", CHAR(36), ForeignKey("Recipient.uuid")))

class User(Base):
    __tablename__= "Users"
    uuid = Column(CHAR(36), primary_key=True)
    firstname = Column(VARCHAR(45))
    lastname = Column(VARCHAR(45))
    fb_access_token = Column(VARCHAR(255))
    fb_email = Column(VARCHAR(45))
    fb_id = Column(BIGINT)
    active = Column(BOOLEAN())
    recipients = relationship("Recipient", secondary=association_table, back_populates="users")

class Recipient(Base):
    __tablename__ = "Recipient"
    uuid = Column(CHAR(36), primary_key=True)
    Users_uuid = Column(CHAR(36), ForeignKey("Users.uuid"))
    users = relationship("User", secondary=association_table, back_populates="recipients")