""" Company scraper data model """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship

Base = declarative_base()

class Company(Base):
    """ Company entity """
    __tablename__ = "Company"
    companyId = Column(String, primary_key=True)
    kununuAccount = relationship("KununuAccount", back_populates="company")
    newsArticles = relationship("NewsArticle", back_populates="company")

class KununuAccount(Base):
    """ Kununu account entity """
    __tablename__ = "KununuAccount"
    kununuAccountId = Column(String, primary_key=True)
    kununuScore = Column(Float, nullable=False)
    companyId = Column(String, ForeignKey("Company.companyId"))
    company = relationship("Company", back_populates="kununuAccount", uselist=False)

class NewsArticle(Base):
    """ Google news article contents entity """
    __tablename__ = "NewsArticles"
    newsArticleId = Column(String, primary_key=True)
    name = Column(String)
    contents = Column(String)
    authorString = Column(String)
    date = Column(DateTime)
    companyId = Column(String, ForeignKey("Company.companyId"))
    company = relationship("Company", back_populates="newsArticles", uselist=False)
