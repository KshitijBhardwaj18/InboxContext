"""User profile for storing writing style preferences"""
from sqlalchemy import Column, String, JSON, Float
from database import Base


class UserProfile(Base):
    """Store user's communication style preferences"""
    __tablename__ = "user_profiles"
    
    id = Column(String, primary_key=True, default="default_user")
    
    # Style preferences learned from edits
    formality_level = Column(Float, default=0.5)  # 0=casual, 1=formal
    avg_response_length = Column(Float, default=75.0)  # Average words
    emoji_usage = Column(Float, default=0.0)  # 0=never, 1=always
    
    # Preferences by sender type
    sender_preferences = Column(JSON, default=dict)  # {investor: {tone: warm, ...}}
    
    # Common patterns
    common_greetings = Column(JSON, default=list)  # ["Hey", "Hi there"]
    common_signoffs = Column(JSON, default=list)  # ["Best", "Cheers"]
    
    # Edit patterns
    tends_to_shorten = Column(Float, default=0.0)  # -1 to 1
    tends_to_casualize = Column(Float, default=0.0)  # -1 to 1
    
    # Metadata
    total_decisions = Column(Float, default=0)
    total_overrides = Column(Float, default=0)

