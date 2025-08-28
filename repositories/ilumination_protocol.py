from typing import Optional
from models.ilumination_protocol import IlluminationProtocol
from models.sampling_point import SamplingPoint
from datetime import datetime, timezone
from db.db import get_db
from sqlalchemy.orm import selectinload


class IlluminationProtocolRepository:
    """Repository for illumination protocol operations"""
    
    @staticmethod
    async def find_by_session_id(session_id: str) -> Optional[IlluminationProtocol]:
        """Find illumination protocol by session_id"""
        db = next(get_db())
        protocol = (
            db.query(IlluminationProtocol)
            .options(selectinload(IlluminationProtocol.sampling_points))
            .filter(IlluminationProtocol.session_id == session_id)
            .first()
        )

        return protocol
    
    @staticmethod
    async def finish_protocol(session_id: str) -> Optional[IlluminationProtocol]:
        """Mark protocol as finished by setting finished_at timestamp"""
        protocol = await IlluminationProtocolRepository.find_by_session_id(session_id)
        if protocol:
            protocol.finished_at = datetime.now(datetime.timezone.utc)
            return await IlluminationProtocolRepository.update(protocol)
        return None
    
    @staticmethod
    async def upsert(protocol: IlluminationProtocol) -> IlluminationProtocol:
        """Upsert illumination protocol based on session_id"""
        db = next(get_db())
        
        # Check if protocol exists for this session
        existing_protocol = (
            db.query(IlluminationProtocol)
            .options(selectinload(IlluminationProtocol.sampling_points))
            .filter(IlluminationProtocol.session_id == protocol.session_id)
            .first()
        )
        
        if existing_protocol:
            # Update existing protocol
            # Copy all fields from the new protocol to the existing one
            for key, value in protocol.__dict__.items():
                if not key.startswith('_') and key != 'id' and key != 'sampling_points':
                    setattr(existing_protocol, key, value)
            
            # Update the updated_at timestamp
            existing_protocol.updated_at = datetime.now(timezone.utc)
            existing_protocol.sampling_points.clear()
            
            incoming_sps = getattr(protocol, "sampling_points", []) or []

            # Romper el vínculo con la lista original para que SQLAlchemy no la toque durante la iteración
            protocol.sampling_points = []   # <- clave

            for sp in list(incoming_sps):   # iterar sobre copia
                sp.id = None
                sp.illumination_protocol = None
                sp.illumination_protocol_id = None

                # Append SIEMPRE vía la colección del padre "existente"
                existing_protocol.sampling_points.append(sp)
            
            db.commit()
            db.refresh(existing_protocol)
            return existing_protocol

        else:
            # Create new protocol
            db.add(protocol)
            db.commit()
            return protocol
