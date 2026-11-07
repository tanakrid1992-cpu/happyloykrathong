import asyncio,json,os,edge_tts
caps=json.load(open("tts/captions.json",encoding="utf-8"))
V={"f":"th-TH-PremwadeeNeural","m":"th-TH-NiwatNeural"}
sem=asyncio.Semaphore(6)
async def one(i,t,g):
    out=f"audio/{g}/{i}.mp3"
    if os.path.exists(out) and os.path.getsize(out)>0: return
    async with sem:
        for _ in range(4):
            try:
                await edge_tts.Communicate(t,V[g],rate="-8%").save(out); return
            except Exception as e: print("retry",i,g,e); await asyncio.sleep(2)
async def main():
    for g in V: os.makedirs(f"audio/{g}",exist_ok=True)
    await asyncio.gather(*[one(i,t,g) for i,t in enumerate(caps) for g in V])
asyncio.run(main())
# rerun to fill missing files
