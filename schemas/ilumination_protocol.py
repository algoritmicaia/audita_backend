from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date, time

class SamplingPoint(BaseModel):
    """Schema for an illumination sampling point"""
    
    # Basic sampling point data
    time: Optional[str] = None  # hora
    sector: Optional[str] = None  # sector
    section: Optional[str] = None  # sección/tipo/puesto
    
    # Illumination type
    illumination_type: Optional[str] = None  # tipo_iluminacion (Natural, Artificial, Mixed)
    source_type: Optional[str] = None  # tipo_fuente (Incandescent, Discharge, Mixed)
    illumination: Optional[str] = None  # iluminacion (General, Localized, Mixed)
    
    # Measurement values
    luminance_uniformity: Optional[str] = None  # uniformidad_luminancia
    average_value: Optional[str] = None  # valor_medio (Average value in Lux)
    required_value: Optional[str] = None  # valor_requerido (Legally required value)


class IluminationProtocol(BaseModel):
    """Complete schema for illumination protocol"""
    
    # Company data
    company_name: Optional[str] = None  # razon_social
    tax_id: Optional[str] = None  # cuit
    address: Optional[str] = None  # direccion
    city: Optional[str] = None  # localidad
    state: Optional[str] = None  # provincia
    postal_code: Optional[str] = None  # codigo_postal
    working_hours: Optional[str] = None  # horarios
    
    # Responsible person data
    first_name: Optional[str] = None  # nombre
    last_name: Optional[str] = None  # apellido
    license_number: Optional[int] = None  # matricula
    
    # Measurement data
    instrument_model_serial: Optional[str] = None  # marca_modelo_nro_serie
    calibration_date: Optional[date] = None  # fecha_calibracion
    methodology: Optional[str] = None  # metodologia
    measurement_date: Optional[date] = None  # fecha_medicion
    measurement_start_time: Optional[str] = None  # hora_inicio_medicion
    measurement_end_time: Optional[str] = None  # hora_fin_medicion
    atmospheric_conditions: Optional[str] = None  # condiciones_atmosfericas
    
    # Sampling points
    sampling_points: Optional[List[SamplingPoint]] = None  # puntos de muestreo
    sampling_observations: Optional[str] = None  # punto_muestreo_observaciones
    
    # Conclusions and recommendations
    conclusions: Optional[str] = None  # conclusiones
    recommendations: Optional[str] = None  # recomendaciones

