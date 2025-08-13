from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class VideoProject(Base):
    """Modelo de la tabla para almacenar la información de cada proyecto de video."""
    __tablename__ = 'video_projects'

    id = Column(Integer, primary_key=True, index=True)
    idea_prompt = Column(Text, nullable=False)
    script = Column(JSON, nullable=True)
    status = Column(String, default='pending', index=True) # pending, generating, editing, publishing, completed, failed
    assets_urls = Column(JSON, nullable=True) # {"images": [...], "audio": "..."}
    final_video_url = Column(String, nullable=True)
    published_urls = Column(JSON, nullable=True) # {"youtube": "...", "tiktok": "..."}
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<VideoProject(id={self.id}, idea='{self.idea_prompt[:30]}...', status='{self.status}')>"


class Idea(Base):
    """Modelo para almacenar ideas de video a ser procesadas."""
    __tablename__ = 'ideas'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False, unique=True)
    # Estados: 'pending', 'processing', 'completed', 'failed'
    status = Column(String, default='pending', index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Idea(id={self.id}, text='{self.text[:30]}...', status='{self.status}')>"
