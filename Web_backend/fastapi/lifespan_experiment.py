'''
Author: WLZ
Date: 2024-04-09 09:20:11
Description: 
'''
from contextlib import asynccontextmanager
import asyncio

def fake_answer_to_everything_ml_model(x: float):
    return x * 42

ml_models = {}

@asynccontextmanager
async def lifespan():
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    print("load")
    yield
    ml_models.clear()
    print("unload")

async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}

async def main(data):
    print(f"model before contextmanager {ml_models}")
    async with lifespan() as lf:
        print(await predict(data))
        print(f"model in contextmanager {ml_models}")
    print(f"model after contextmanager {ml_models}")

if __name__ == "__main__":
    asyncio.run(main(10))

