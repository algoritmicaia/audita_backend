from typing import Optional, List
from models.ilumination_protocol import IlluminationProtocol
from models.sampling_point import SamplingPoint
from repositories.ilumination_protocol import IlluminationProtocolRepository
from datetime import datetime


class IlluminationProtocolService:
    """Service for illumination protocol business logic"""
    
    @staticmethod
    async def upsert_protocol(protocol: IlluminationProtocol) -> IlluminationProtocol:
        """
        Upsert illumination protocol based on session_id.
        If protocol exists for the session_id, update it. Otherwise, create new one.
        """
        # Check if protocol exists for this session
        existing_protocol = await IlluminationProtocolRepository.find_by_session_id(protocol.session_id)
        
        if existing_protocol:
            # Update existing protocol
            # Copy all fields from the new protocol to the existing one
            for key, value in protocol.__dict__.items():
                if not key.startswith('_') and key != 'id' and key != 'created_at':
                    setattr(existing_protocol, key, value)
            
            # Update the updated_at timestamp
            existing_protocol.updated_at = datetime.now(datetime.timezone.utc)
            
            return await IlluminationProtocolRepository.update(existing_protocol)
        else:
            # Create new protocol
            return await IlluminationProtocolRepository.create(protocol)
    
    @staticmethod
    async def get_protocol_by_session_id(session_id: str) -> Optional[IlluminationProtocol]:
        """Get illumination protocol by session_id"""
        return await IlluminationProtocolRepository.find_by_session_id(session_id)
    
   