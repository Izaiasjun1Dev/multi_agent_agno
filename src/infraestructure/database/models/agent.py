
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String, Text, JSON
from sqlalchemy.orm import relationship

from infraestructure.database.config import Base


class Agent(Base):
    __tablename__ = "agents"
    agent_id = Column(String(36), primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    configs = Column(JSON, nullable=True)  # Store configurations as JSON
    tools = Column(JSON, nullable=True)  # Store tools as JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Agent(agent_id='{self.agent_id}', name='{self.name}')>"
    
    
    