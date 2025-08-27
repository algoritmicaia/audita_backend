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
            
            # Handle sampling points if provided
            if hasattr(protocol, 'sampling_points') and protocol.sampling_points:
                # Delete existing sampling points for this protocol
                db.query(SamplingPoint).filter(
                    SamplingPoint.illumination_protocol_id == existing_protocol.id
                ).delete()
                
                # Add new sampling points
                for sampling_point in protocol.sampling_points:
                    sampling_point.illumination_protocol_id = existing_protocol.id
                    sampling_point.session_id = existing_protocol.session_id
                    db.add(sampling_point)
            
            db.commit()
            return existing_protocol
        else:
            # Create new protocol
            db.add(protocol)
            db.commit()
            return protocol
