from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class JiraIssue(Base):
    __tablename__ = "jiraissue"
    id = Column(Integer, primary_key=True, index=True)
    issuenum = Column(Integer)
    project = Column(Integer, ForeignKey("project.id"))
    issuetype = Column(Integer, ForeignKey("issuetype.id"))
    summary = Column(String)
    description = Column(Text)
    priority = Column(Integer, ForeignKey("priority.id"))
    resolution = Column(Integer, ForeignKey("resolution.id"))
    issuestatus = Column(Integer, ForeignKey("issuestatus.id"))
    created = Column(DateTime)
    updated = Column(DateTime)
    duedate = Column(DateTime)
    resolutiondate = Column(DateTime)
    archived = Column(String)

    status = relationship("IssueStatus", back_populates="issues")

class IssueType(Base):
    __tablename__ = "issuetype"
    id = Column(Integer, primary_key=True)
    pname = Column(String)

class Project(Base):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    pname = Column(String)
    lead = Column(String)
    pkey = Column(String)

class ProjectKey(Base):
    __tablename__ = "project_key"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    project_key = Column(String)

class Priority(Base):
    __tablename__ = "priority"
    id = Column(Integer, primary_key=True)
    pname = Column(String)

class Resolution(Base):
    __tablename__ = "resolution"
    id = Column(Integer, primary_key=True)
    pname = Column(String)

class IssueStatus(Base):
    __tablename__ = "issuestatus"
    id = Column(Integer, primary_key=True)
    pname = Column(String)
    issues = relationship("JiraIssue", back_populates="status")

class JiraAction(Base):
    __tablename__ = "jiraaction"
    id = Column(Integer, primary_key=True)
    issueid = Column(Integer, ForeignKey("jiraissue.id"))
    author = Column(String)
    body = Column(Text)
    created = Column(DateTime)