import base64
import secrets
from typing import List
from fastapi import APIRouter, HTTPException, Request, Depends
from starlette import status
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils

from api.dependecies.security import api_key_auth, get_current_user
from models.client import Client_Pydantic, ClientModel, ClientIn_Pydantic, StatusEnum
from models.client import KeyModel, APIKey_Pydantic
from models.manager import Manager_Pydantic
from schemas.client import Message, CountChange

router = APIRouter()


async def get_key(key):
    open("key", "w").write(key)
    with open('key', 'rb') as keyfile:
        key = serialization.load_pem_private_key(keyfile.read(), password=None)
    return key


@router.get('/', response_model=List[Client_Pydantic])
async def list_all_clients():
    return await Client_Pydantic.from_queryset(ClientModel.all())


@router.post('/', response_model=Client_Pydantic)
async def create_client(client: ClientIn_Pydantic):
    client_obj = await ClientModel.create(**client.dict(exclude_unset=True))
    return await Client_Pydantic.from_tortoise_orm(client_obj)


@router.post('/sign_message')
async def sign_message(message: Message, client: Client_Pydantic = Depends(api_key_auth)):
    try:
        sign_key = await get_key(client.key)

        message_bytes = base64.b64decode(message.message)
        signature = sign_key.sign(message_bytes, padding.PKCS1v15(), utils.Prehashed(hashes.SHA1()))
        signed_message = base64.b64encode(signature).decode()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': f'{e}'})
    client = await ClientModel.get(id=client.id)
    if client.status == StatusEnum.BLOCKED:
        return {'status': 'bad request', 'message': 'Blocked'}
    if client.count <= 0:
        return {'status': 'bad request', 'message': 'Count below 1'}
    client.count -= 1
    await client.save()
    return {'status': 'ok', 'message': signed_message}


@router.patch('/count/{client_id}', response_model=Client_Pydantic)
async def edit_client_count(client_id: int, data: CountChange):
    try:
        client = await ClientModel.get(id=client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not existing client.')
        client.count = data.count
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': e.args})
    await client.save()
    return await Client_Pydantic.from_tortoise_orm(client)


@router.patch('/block_client/{client_id}')
async def block_client(client_id: int, manager: Manager_Pydantic = Depends(get_current_user)):
    client = await ClientModel.get(id=client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not existing client.')
    if client.status == StatusEnum.BLOCKED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Client already blocked.')
    client.status = StatusEnum.BLOCKED
    await client.save()
    return await Client_Pydantic.from_tortoise_orm(client)


@router.patch('/unblock_client/{client_id}')
async def unblock_client(client_id: int, manager: Manager_Pydantic = Depends(get_current_user)):
    client = await ClientModel.get(id=client_id)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not existing client.')
    if client.status == StatusEnum.ACTIVE:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Client not blocked.')
    client.status = StatusEnum.ACTIVE
    await client.save()
    return await Client_Pydantic.from_tortoise_orm(client)


@router.get('/api_key/{client_id}', response_model=APIKey_Pydantic)
async def generate_api_key(client_id: int, manager: Manager_Pydantic = Depends(get_current_user)):
    client = await ClientModel.filter(id=client_id).get()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not existing client.')
    api_key = await KeyModel.get_or_none(client=client)
    if not api_key:
        api_key = await KeyModel.create(client=client, api_key=secrets.token_urlsafe(32))
    api_key.api_key = secrets.token_urlsafe(32)
    await api_key.save()
    return await APIKey_Pydantic.from_tortoise_orm(api_key)
