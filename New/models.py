from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class JiraIssue(Base):
    __tablename__ = "jiraissue"

    id = Column(Integer, primary_key=True, index=True)
    issuenum = Column(Integer)
    project = Column(Integer, ForeignKey("project.id"))
    summary = Column(String)
    description = Column(String)
    issuestatus = Column(Integer, ForeignKey("issuestatus.id"))
    priority = Column(Integer, ForeignKey("priority.id"))
    archived = Column(String)  # Expecting 'Y' or 'N'

    project_rel = relationship("Project")
    status_rel = relationship("IssueStatus")
    priority_rel = relationship("Priority")
    comments = relationship("JiraAction", back_populates="issue")


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    pname = Column(String)
    issues = relationship("JiraIssue", back_populates="project_rel")


class IssueStatus(Base):
    __tablename__ = "issuestatus"

    id = Column(Integer, primary_key=True)
    pname = Column(String)


class Priority(Base):
    __tablename__ = "priority"

    id = Column(Integer, primary_key=True)
    pname = Column(String)


class JiraAction(Base):
    __tablename__ = "jiraaction"

    id = Column(Integer, primary_key=True, index=True)
    issueid = Column(Integer, ForeignKey("jiraissue.id"))
    actiontype = Column(String)
    author = Column(String)
    actionbody = Column(String)
    created = Column(DateTime)

    issue = relationship("JiraIssue", back_populates="comments")
