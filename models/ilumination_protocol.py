from datetime import timezone
from sqlalchemy import Column, Integer, String, DateTime, Date, Text
from sqlalchemy.orm import relationship
from db.db import Base
from datetime import datetime


class IlluminationProtocol(Base):
    """Domain model for illumination protocol"""
    
    __tablename__ = "illumination_protocols"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Session tracking
    session_id = Column(String(100), nullable=False)
    
    # Company data
    company_name = Column(String(200), nullable=True)  # razon_social
    tax_id = Column(String(20), nullable=True)  # cuit
    address = Column(String(300), nullable=True)  # direccion
    city = Column(String(100), nullable=True)  # localidad
    state = Column(String(100), nullable=True)  # provincia
    postal_code = Column(String(10), nullable=True)  # codigo_postal
    working_hours = Column(String(100), nullable=True)  # horarios
    
    # Responsible person data
    first_name = Column(String(100), nullable=True)  # nombre
    last_name = Column(String(100), nullable=True)  # apellido
    license_number = Column(Integer, nullable=True)  # matricula
    
    # Measurement data
    instrument_model_serial = Column(String(200), nullable=True)  # marca_modelo_nro_serie
    calibration_date = Column(Date, nullable=True)  # fecha_calibracion
    methodology = Column(Text, nullable=True)  # metodologia
    measurement_date = Column(Date, nullable=True)  # fecha_medicion
    measurement_start_time = Column(String(10), nullable=True)  # hora_inicio_medicion
    measurement_end_time = Column(String(10), nullable=True)  # hora_fin_medicion
    atmospheric_conditions = Column(Text, nullable=True)  # condiciones_atmosfericas
    
    # Sampling points observations
    sampling_observations = Column(Text, nullable=True)  # punto_muestreo_observaciones
    
    # Conclusions and recommendations
    conclusions = Column(Text, nullable=True)  # conclusiones
    recommendations = Column(Text, nullable=True)  # recomendaciones
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    finished_at = Column(DateTime, nullable=True)
    
    # Relationships
    sampling_points = relationship("SamplingPoint", back_populates="illumination_protocol", cascade="all, delete-orphan", uselist=True)
    
    def __repr__(self):
        return f"<IlluminationProtocol(id={self.id}, company_name={self.company_name})>"
