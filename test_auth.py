#!/usr/bin/env python3
"""Script de test para el endpoint de autenticación."""

import httpx
import json

async def test_request_code():
    """Prueba el endpoint /auth/request-code."""
    url = "http://localhost:8000/auth/request-code"

    payload = {"cuit": "30-12345678-9"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=30.0)

            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"\nResponse:")

            try:
                print(json.dumps(response.json(), indent=2))
            except:
                print(response.text)

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_request_code())
