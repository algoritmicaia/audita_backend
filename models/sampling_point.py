from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.db import Base
from sqlalchemy.sql import func


class SamplingPoint(Base):
    """Domain model for illumination sampling point"""
    
    __tablename__ = "sampling_points"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to illumination protocol
    illumination_protocol_id = Column(Integer, ForeignKey("illumination_protocols.id"), nullable=False)
    
    # Basic sampling point data
    time = Column(String(10), nullable=True)  # hora
    sector = Column(String(100), nullable=True)  # sector
    section = Column(String(100), nullable=True)  # sección/tipo/puesto
    
    # Illumination type
    illumination_type = Column(String(50), nullable=True)  # tipo_iluminacion (Natural, Artificial, Mixed)
    source_type = Column(String(50), nullable=True)  # tipo_fuente (Incandescent, Discharge, Mixed)
    illumination = Column(String(50), nullable=True)  # iluminacion (General, Localized, Mixed)
    
    # Measurement values
    luminance_uniformity = Column(String(50), nullable=True)  # uniformidad_luminancia
    average_value = Column(String(50), nullable=True)  # valor_medio (Average value in Lux)
    required_value = Column(String(50), nullable=True)  # valor_requerido (Legally required value)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    finished_at = Column(DateTime, nullable=True)
    
    # Relationship
    illumination_protocol = relationship("IlluminationProtocol", back_populates="sampling_points")
    
    def __repr__(self):
        return f"<SamplingPoint(id={self.id}, sector={self.sector}, section={self.section})>"
