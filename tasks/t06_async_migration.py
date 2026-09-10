# Task 6: Synchronous to Async Pipeline
import asyncio

async def fetch_data_async(source_id: int):
    await asyncio.sleep(0.01)
    return {"id": source_id, "data": f"content_{source_id}"}

async def process_all_sources(source_ids: list):
    tasks = [fetch_data_async(sid) for sid in source_ids]
    results = await asyncio.gather(*tasks, return_exceptions=False)
    return results
