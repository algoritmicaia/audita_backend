from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from models.ilumination_protocol import IlluminationProtocol
from models.sampling_point import SamplingPoint
from datetime import datetime
from db.db import session_scope


class IlluminationProtocolRepository:
    """Repository for illumination protocol operations"""
    
    @staticmethod
    async def find_by_session_id(session_id: str) -> Optional[IlluminationProtocol]:
        """Find illumination protocol by session_id"""
        with session_scope() as db:
            return db.query(IlluminationProtocol).filter(
                IlluminationProtocol.session_id == session_id
            ).first()
    
    @staticmethod
    async def create(protocol: IlluminationProtocol) -> IlluminationProtocol:
        """Create a new illumination protocol with sampling points"""
        with session_scope() as db:
            # Extract sampling points from protocol if they exist
            sampling_points = protocol.sampling_points if hasattr(protocol, 'sampling_points') else []
            protocol.sampling_points = []  # Clear to avoid duplicate insertion
            
            # Add protocol to session
            db.add(protocol)
            db.flush()  # Flush to get the protocol ID
            
            # Add sampling points with the protocol ID
            for sampling_point in sampling_points:
                sampling_point.illumination_protocol_id = protocol.id
                sampling_point.session_id = protocol.session_id
                db.add(sampling_point)
            
            db.refresh(protocol)
            return protocol
    
    @staticmethod
    async def update(protocol: IlluminationProtocol) -> IlluminationProtocol:
        """Update an existing illumination protocol with sampling points"""
        with session_scope() as db:

        
            # Get existing protocol from database
            existing_protocol = db.query(IlluminationProtocol).filter(
                IlluminationProtocol.id == protocol.id
            ).first()
            
            if not existing_protocol:
                raise ValueError(f"Protocol with id {protocol.id} not found")
            
            # Update protocol fields
            for key, value in protocol.__dict__.items():
                if not key.startswith('_') and key != 'id' and key != 'sampling_points':
                    setattr(existing_protocol, key, value)
            
            existing_protocol.updated_at = datetime.now(datetime.timezone.utc)
            
            # Handle sampling points if provided
            if hasattr(protocol, 'sampling_points') and protocol.sampling_points:
                # Delete existing sampling points for this protocol
                db.query(SamplingPoint).filter(
                    SamplingPoint.illumination_protocol_id == protocol.id
                ).delete()
                
                # Add new sampling points
                for sampling_point in protocol.sampling_points:
                    sampling_point.illumination_protocol_id = protocol.id
                    sampling_point.session_id = protocol.session_id
                    db.add(sampling_point)
            
            db.refresh(existing_protocol)
            return existing_protocol
        
    @staticmethod
    async def finish_protocol(session_id: str) -> Optional[IlluminationProtocol]:
        """Mark protocol as finished by setting finished_at timestamp"""
        protocol = await IlluminationProtocolRepository.find_by_session_id(session_id)
        if protocol:
            protocol.finished_at = datetime.now(datetime.timezone.utc)
            return await IlluminationProtocolRepository.update(protocol)
        return None
