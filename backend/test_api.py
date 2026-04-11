import httpx
import asyncio
import os

async def run():
    async with httpx.AsyncClient() as client:
        # GET /
        r1 = await client.get('http://127.0.0.1:8000/')
        print("GET /:", r1.json())
        
        # Write temporary csv
        with open("test.csv", "w") as f:
            f.write("A,B\n1,2\n3,4\n")
            
        # POST /upload
        with open("test.csv", "rb") as f:
            r2 = await client.post('http://127.0.0.1:8000/upload', files={'file': ('test.csv', f, 'text/csv')})
            print("POST /upload:", r2.json())
            
        file_id = r2.json().get('data', {}).get('file_id')
        if file_id:
            # POST /analyze
            r3 = await client.post('http://127.0.0.1:8000/analyze', json={'file_id': file_id})
            print("POST /analyze:", r3.json())

asyncio.run(run())
