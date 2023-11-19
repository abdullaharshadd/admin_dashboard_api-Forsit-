import os
from fastapi import FastAPI, Depends, HTTPException, Header
from jose import JWTError, jwt
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from typing import Optional
import httpx
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from base64 import b64decode
from cryptography.hazmat.primitives.serialization import load_der_public_key
import base64
import json
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

AUTH0_DOMAIN = config['auth0']['AUTH0_DOMAIN']
AUTH0_AUDIENCE = config['auth0']['AUTH0_AUDIENCE']
CLIENT_ID = config['auth0']['CLIENT_ID']
CLIENT_SECRET = config['auth0']['CLIENT_SECRET']
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"


import http.client

async def get_access_token():
    try:
        conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
        payload = f"{{\"client_id\":\"{CLIENT_ID}\",\"client_secret\":\"{CLIENT_SECRET}\",\"audience\":\"{AUTH0_AUDIENCE}\",\"grant_type\":\"client_credentials\"}}"  
        headers = { 'content-type': "application/json" }
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))["access_token"]
    except:
        print("Error while getting the access token")
        return None

async def get_public_key(jwks_url: str = JWKS_URL, kid: str = None):
    async with httpx.AsyncClient() as client:
        jwks = await client.get(jwks_url)
        jwks.raise_for_status()
        jwks_data = jwks.json()

    # Retrieve the RSA public key
    rsa_key = next((key for key in jwks_data["keys"] if key["kid"] == kid), None)
    if rsa_key is None:
        raise HTTPException(status_code=404, detail="Public key not found")

    pem_key = f"-----BEGIN CERTIFICATE-----\n{rsa_key['x5c'][0]}\n-----END CERTIFICATE-----"
    cert = load_pem_x509_certificate(pem_key.encode(), default_backend())
    public_key = cert.public_key()

    return public_key

async def validate_requester(
    authorization: Optional[str] = Header(None, alias="Authorization")
): 
    print(AUTH0_AUDIENCE)
    credentials_exception = HTTPException(
        status_code=401,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if authorization is None:
        raise credentials_exception
    token = authorization.split(" ")[1]
    try:
        # Extract 'kid' from the decoded token header
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")

        # Validate the token with the correct 'kid'
        public_key = await get_public_key(JWKS_URL, kid)  # Await the result here
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=AUTH0_AUDIENCE,
            issuer=AUTH0_ISSUER,
        )
        return payload
    except JWTError:
        raise credentials_exception
