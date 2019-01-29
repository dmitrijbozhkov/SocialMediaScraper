""" Description of database model """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

xing_account_have = Table("XingAccountHave", Base.metadata,
    Column("xingAccountId", Integer, ForeignKey("XingAccount.xingAccountId")),
    Column("xingHaveId", Integer, ForeignKey("XingHave.xingHaveId"))
)

class XingHave(Base):
    __tablename__ = "XingHave"
    xingHaveId = Column(Integer, primary_key=True, autoincrement=True)
    haveName = Column(String)
    xingAccounts = relationship("XingAccount", secondary=xing_account_have, back_populates="xingHaves")

xing_account_want = Table("XingAccountWant", Base.metadata,
    Column("xingAccountId", Integer, ForeignKey("XingAccount.xingAccountId")),
    Column("xingWantId", Integer, ForeignKey("XingWant.xingWantId"))
)

class XingWant(Base):
    __tablename__ = "XingWant"
    xingWantId = Column(Integer, primary_key=True, autoincrement=True)
    wantName = Column(String)
    xingAccounts = relationship("XingAccount", secondary=xing_account_want, back_populates="xingWants")

class XingWorkExperience(Base):
    __tablename__ = "XingWorkExperience"
    xingWorkExperienceId = Column(Integer, primary_key=True, autoincrement=True)
    position = Column(String)
    companyName = Column(String)
    beginDate = Column(String)
    endDate = Column(String)
    timeWorked = Column(String)
    industry = Column(String)
    organisationType = Column(String)
    employess = Column(String)
    employment = Column(String)
    timeWorked = Column(String)
    careerLevel = Column(String)
    discipline = Column(String)
    xingAccountId = Column(Integer, ForeignKey("XingAccount.xingAccountId"))
    xingAccount = relationship("XingAccount", back_populates="xingWorkExperiences")

class XingAccount(Base):
    """ Table for Xing accounts """
    __tablename__ = "XingAccount"
    xingAccountId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    currentPosition = Column(String)
    locaton = Column(String)
    person = relationship("Person", back_populates="xingAccount", uselist=False)
    xingWorkExperiences = relationship("XingWorkExperience", back_populates="xingAccount")
    xingHaves = relationship("XingHave", secondary=xing_account_have, back_populates="xingAccounts")
    xingWants = relationship("XingWant", secondary=xing_account_want, back_populates="xingAccounts")

class LinkedInEducation(Base):
    __tablename__ = "LinkedInEducation"
    linkedInEducationId = Column(Integer, primary_key=True, autoincrement=True)
    facilityName = Column(String)
    degreeName = Column(String)
    beginDate = Column(String)
    endDate = Column(String)
    linkedInAccountId = Column(Integer, ForeignKey("LinkedInAccount.linkedInAccountId"))
    linkedInAccount = relationship("LinkedInAccount", back_populates="linkedInEducation")

class LinkedInWorkExperience(Base):
    __tablename__ = "LinkedInWorkExperience"
    linkedInWorkExperienceId = Column(Integer, primary_key=True, autoincrement=True)
    position = Column(String)
    companyName = Column(String)
    beginDate = Column(String)
    endDate = Column(String)
    timeWorked = Column(String)
    location = Column(String)
    description = Column(String)
    linkedInAccountId = Column(Integer, ForeignKey("LinkedInAccount.linkedInAccountId"))
    linkedInAccount = relationship("LinkedInAccount", back_populates="linkedInWorkExperiences")

class LinkedInAccount(Base):
    """ Table for LinkedIn accounts """
    __tablename__ = "LinkedInAccount"
    linkedInAccountId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    currentPosition = Column(String)
    locaton = Column(String)
    person = relationship("Person", back_populates="linkedInAccount", uselist=False)
    linkedInWorkExperiences = relationship("LinkedInWorkExperience", back_populates="linkedInAccount")
    linkedInEducation = relationship("LinkedInEducation", back_populates="linkedInAccount")

class TwitterAccountDetails(Base):
    __tablename__ = "TwitterAccountDetails"
    twitterAccountDetailsId = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    location = Column(String)
    registerDate = Column(String)
    amountTweets = Column(Integer)
    amountSubscriptions = Column(Integer)
    amountSubscribers = Column(Integer)
    amountLikes = Column(Integer)
    twitterAccount = relationship("TwitterAccount", back_populates="twitterAccountDetails")

class Tweet(Base):
    __tablename__ = "Tweet"
    tweetId = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    datetime = Column(DateTime)
    isOriginal = Column(Boolean)
    amountComments = Column(Integer)
    amountRetweets = Column(Integer)
    amountLikes = Column(Integer)
    twitterAccountId = Column(Integer, ForeignKey("TwitterAccount.twitterAccountId"))
    twitterAccount = relationship("TwitterAccount", back_populates="tweets")

class TwitterAccount(Base):
    """ Table for Twitter accounts """
    __tablename__ = "TwitterAccount"
    twitterAccountId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    atName = Column(String, nullable=False)
    person = relationship("Person", back_populates="twitterAccount", uselist=False)
    twitterAccountDetailsId = Column(Integer, ForeignKey("TwitterAccountDetails.twitterAccountDetailsId"))
    twitterAccountDetails = relationship("TwitterAccountDetails", back_populates="twitterAccount", uselist=False)
    tweets = relationship("Tweet", back_populates="twitterAccount")

class Person(Base):
    """ Table, that represents a person, whose data should be scraped """
    __tablename__ = "Person"
    personId = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    twitterAccountId = Column(Integer, ForeignKey("TwitterAccount.twitterAccountId"))
    twitterAccount = relationship("TwitterAccount", back_populates="person", uselist=False)
    linkedInAccountId = Column(Integer, ForeignKey("LinkedInAccount.linkedInAccountId"))
    linkedInAccount = relationship("LinkedInAccount", back_populates="person", uselist=False)
    xingAccountId = Column(Integer, ForeignKey("XingAccount.xingAccountId"))
    xingAccount = relationship("XingAccount", back_populates="person", uselist=False)
