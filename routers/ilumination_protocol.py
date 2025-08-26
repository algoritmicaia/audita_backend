from typing import Optional
import uuid
from fastapi import APIRouter, Cookie, Depends, Response

from schemas.ilumination_protocol import IluminationProtocol
from models.ilumination_protocol import IlluminationProtocol
from models.sampling_point import SamplingPoint
from services.ilumination_protocol import IlluminationProtocolService

ilumination_protocol_router = APIRouter()

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


@ilumination_protocol_router.post("/ilumination_protocol")
async def save_protocol(
    protocol_data: IluminationProtocol, 
    response: Response,
    session_id: str = Depends(get_session_id)
    ):
    """
    Save or update illumination protocol based on session_id.
    If protocol exists for the session_id, it will be updated. Otherwise, a new one will be created.
    """
    
    # Set session_id cookie
    response.set_cookie(
        key="session_id", 
        value=session_id, 
        httponly=True,
        secure=True,
    )
    
    try:
        # Convert schema to domain model
        protocol_dict = protocol_data.model_dump(mode='json')
        
        # Extract sampling points data
        sampling_points_data = protocol_dict.pop('sampling_points', [])
        
        # Add session_id to the protocol data
        protocol_dict['session_id'] = session_id
        
        # Create domain model instance without sampling points
        protocol_domain = IlluminationProtocol(**protocol_dict)
        
        # Create sampling points domain models
        sampling_points = []
        for sp_data in sampling_points_data:
            sp_data['session_id'] = session_id
            sampling_point = SamplingPoint(**sp_data)
            sampling_points.append(sampling_point)
        
        # Assign sampling points to protocol
        protocol_domain.sampling_points = sampling_points
        
        # Call service to upsert protocol
        saved_protocol = await IlluminationProtocolService.upsert_protocol(protocol_domain)
        
        return {
            'result': 'success',
            'protocol_id': saved_protocol.id,
            'session_id': session_id,
            'message': 'Protocol saved successfully'
        }
        
    except Exception as e:
        return {
            'result': 'error',
            'message': f'Error saving protocol: {str(e)}'
        }

