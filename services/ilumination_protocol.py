from typing import Optional, List
from models.ilumination_protocol import IlluminationProtocol
from models.sampling_point import SamplingPoint
from repositories.ilumination_protocol import IlluminationProtocolRepository
from datetime import datetime, timezone


class IlluminationProtocolService:
    """Service for illumination protocol business logic"""
    
    @staticmethod
    async def upsert_protocol(protocol: IlluminationProtocol) -> IlluminationProtocol:
        """
        Upsert illumination protocol based on session_id.
        If protocol exists for the session_id, update it. Otherwise, create new one.
        """
        return await IlluminationProtocolRepository.upsert(protocol)
        
    
    @staticmethod
    async def get_protocol_by_session_id(session_id: str) -> Optional[IlluminationProtocol]:
        """Get illumination protocol by session_id"""
        return await IlluminationProtocolRepository.find_by_session_id(session_id)
    
   