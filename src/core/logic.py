import httpx

async def forward_request(url, headers, params, method, data=None):
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            content=data
        )
        return response
