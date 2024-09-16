from sqlalchemy import Column, Integer, String, DateTime, Sequence, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
import uuid
from sqlalchemy.orm import relationship

import humanize

Base = declarative_base()
class Flow(Base):
    __tablename__ = 'flows'
    
    id = Column(Integer, Sequence('flow_id_seq'), primary_key=True)
    flow_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    name = Column(String(100), nullable=False)
    entry_point = Column(String(255), nullable=False)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flow_runs = relationship("FlowRuns")

    def to_dict(self):
        return {
            'id'         : self.id,
            'flow_id'    : str(self.flow_id),
            'name'       : self.name,
            'entry_point': self.entry_point,
            'tags'       : self.tags,
            'created_at' : str(self.created_at),
            'updated_at' : str(self.updated_at)
        }

class FlowRuns(Base):
    __tablename__ = 'flow_runs'
    
    id = Column(Integer, Sequence('flow_runs_id_seq'), primary_key=True)
    flow_run_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    name = Column(String(100), nullable=False)
    flow_id = Column(UUID(as_uuid=True), ForeignKey('flows.flow_id'))
    status = Column(String(255), nullable=False, default="QUEUED")

    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flow = relationship("Flow")
    task_runs = relationship("TaskRuns")


    def to_dict(self):
        return {
            'id'         : self.id,
            'flow_run_id': str(self.flow_run_id),
            'name'       : self.name,
            'flow_id'    : str(self.flow_id),
            'status'     : self.status,
            'duration'   : self.calculate_duration(),
            'flow'       : self.flow.to_dict() if self.flow else None,
            # 'task_runs': [task_run.to_dict() for task_run in self.task_runs]
        }

    def calculate_duration(self):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return humanize.naturaldelta(delta)
        return None

class TaskRuns(Base):
    __tablename__ = 'task_runs'
    
    id = Column(Integer, Sequence('task_runs_id_seq'), primary_key=True)
    task_run_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    name = Column(String(100), nullable=False)
    flow_run_id = Column(UUID(as_uuid=True), ForeignKey('flow_runs.flow_run_id'))
    status = Column(String(255), nullable=False, default="QUEUED")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flow_run = relationship("FlowRuns")


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