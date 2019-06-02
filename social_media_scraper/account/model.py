""" Description of database model """
from collections import namedtuple
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()

class XingEducation(Base):
    __tablename__ = "XingEducation"
    xingEducationId = Column(Integer, primary_key=True, autoincrement=True)
    degree = Column(String)
    schoolName = Column(String)
    subject = Column(String)
    schoolNotes = Column(String)
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    xingAccountId = Column(String, ForeignKey("XingAccount.xingAccountId"))
    xingAccount = relationship("XingAccount", back_populates="xingEducations")

class XingWorkExperience(Base):
    __tablename__ = "XingWorkExperience"
    xingWorkExperienceId = Column(Integer, primary_key=True, autoincrement=True)
    position = Column(String)
    companyName = Column(String)
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    xingAccountId = Column(String, ForeignKey("XingAccount.xingAccountId"))
    xingAccount = relationship("XingAccount", back_populates="xingWorkExperiences")

class XingAccount(Base):
    """ Table for Xing accounts """
    __tablename__ = "XingAccount"
    xingAccountId = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    currentPosition = Column(String)
    locaton = Column(String)
    haves = Column(String)
    wants = Column(String)
    person = relationship("Person", back_populates="xingAccount", uselist=False)
    xingEducations = relationship("XingEducation", back_populates="xingAccount")
    xingWorkExperiences = relationship("XingWorkExperience", back_populates="xingAccount")

class LinkedInEducation(Base):
    __tablename__ = "LinkedInEducation"
    linkedInEducationId = Column(Integer, primary_key=True, autoincrement=True)
    facilityName = Column(String)
    degreeName = Column(String)
    specialtyName = Column(String)
    dateRange = Column(String)
    linkedInAccountId = Column(String, ForeignKey("LinkedInAccount.linkedInAccountId"))
    linkedInAccount = relationship("LinkedInAccount", back_populates="linkedInEducations")

class LinkedInWorkExperience(Base):
    __tablename__ = "LinkedInWorkExperience"
    linkedInWorkExperienceId = Column(Integer, primary_key=True, autoincrement=True)
    position = Column(String)
    companyName = Column(String)
    dateRange = Column(String)
    timeWorked = Column(String)
    location = Column(String)
    description = Column(String)
    linkedInAccountId = Column(String, ForeignKey("LinkedInAccount.linkedInAccountId"))
    linkedInAccount = relationship("LinkedInAccount", back_populates="linkedInWorkExperiences")

class LinkedInAccount(Base):
    """ Table for LinkedIn accounts """
    __tablename__ = "LinkedInAccount"
    linkedInAccountId = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    currentPosition = Column(String)
    locaton = Column(String)
    person = relationship("Person", back_populates="linkedInAccount", uselist=False)
    linkedInWorkExperiences = relationship("LinkedInWorkExperience", back_populates="linkedInAccount")
    linkedInEducations = relationship("LinkedInEducation", back_populates="linkedInAccount")

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
    twitterAccountId = Column(String, ForeignKey("TwitterAccount.twitterAccountId"))
    twitterAccount = relationship("TwitterAccount", back_populates="tweets")

class TwitterAccount(Base):
    """ Table for Twitter accounts """
    __tablename__ = "TwitterAccount"
    twitterAccountId = Column(String, primary_key=True)
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
    twitterAccountId = Column(String, ForeignKey("TwitterAccount.twitterAccountId"))
    twitterAccount = relationship("TwitterAccount", back_populates="person", uselist=False)
    linkedInAccountId = Column(String, ForeignKey("LinkedInAccount.linkedInAccountId"))
    linkedInAccount = relationship("LinkedInAccount", back_populates="person", uselist=False)
    xingAccountId = Column(String, ForeignKey("XingAccount.xingAccountId"))
    xingAccount = relationship("XingAccount", back_populates="person", uselist=False)
