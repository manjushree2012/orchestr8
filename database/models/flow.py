from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
import uuid

Base = declarative_base()
class Flow(Base):
    __tablename__ = 'flows'
    
    id = Column(Integer, Sequence('flow_id_seq'), primary_key=True)
    flow_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    name = Column(String(100), nullable=False)
    entry_point = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FlowRuns(Base):
    __tablename__ = 'flow_runs'
    
    id = Column(Integer, Sequence('flow_runs_id_seq'), primary_key=True)
    flow_run_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    name = Column(String(100), nullable=False)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.flow_id'))
    status = Column(String(255), nullable=False, default="QUEUED")

    start_time = Column(DateTime, nullable=True)  # new field
    end_time = Column(DateTime, nullable=True)  # new field

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TaskRuns(Base):
    __tablename__ = 'task_runs'
    
    id = Column(Integer, Sequence('task_runs_id_seq'), primary_key=True)
    task_run_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    name = Column(String(100), nullable=False)
    flow_run_id = Column(UUID(as_uuid=True), ForeignKey('flow_runs.flow_run_id'))
    status = Column(String(255), nullable=False, default="QUEUED")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, Sequence('logs_id_seq'), primary_key=True)
    log_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)

    flow_run_id = Column(UUID(as_uuid=True), ForeignKey('flow_runs.flow_run_id'), nullable=True)
    task_run_id = Column(UUID(as_uuid=True), ForeignKey('task_runs.task_run_id'), nullable=True)

    level = Column(String(50), nullable=False)  # e.g., DEBUG, INFO, WARNING, ERROR
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)