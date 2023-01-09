#/usr/bin/env python3
import json
import os
import os.path
import re

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# import time


# from fastapi.middleware.cors import CORSMiddleware
# from fastapi_utils.tasks import repeat_every

__api_version__ = 1


ascii = re.compile("([a-z]+)([0-9]+)")


def ostype():
    try:
        with open("/etc/os-release") as f:
            lines = [line for line in f if line.find("PRETTY_NAME") >= 0]
            return lines[0].split("=")[1].strip('"\n')
    except:
        with open("/etc/system-release") as f:
            return f.readline().strip()


def get_spec():
    """
    for a linuxy system
    """
    try:
        with open("/proc/cpuinfo") as f:
            lines = [line for line in f if line.find("bogomips") == 0]
            bogomips = [float(x.split(":")[1].strip()) for x in lines]
            cores = len(bogomips)
            mips = sum(bogomips) / cores
            return {
                "cores": cores,
                "mips":  mips,
            }
    except:
        return {}


def loadavg():
    with open("/proc/loadavg") as f:
        return float(f.readline().split()[0])


def info():
    output = get_spec()
    output["load"] = loadavg()
    output["ostype"] = ostype()
    print(output)
    return json.dumps(output)



app = FastAPI()
api = FastAPI(root_path=f"/v{__api_version__}")
app.mount(f"/v{__api_version__}", api)
# app.mount("/", StaticFiles(directory="../loadmeters/public", html=True), name="static")



# @app.on_event("startup")
# @repeat_every(seconds=15)  # 15 seconds
# def update_history() -> None:
#     fn = "history.json"
#     try:
#         with open(fn) as f:
#             history = json.load(f)
#     except:
#         history = {}
#     with os.popen("ruptime -a","r") as pipe:
#         for line in pipe:
#             columns = line.split()
#             server = columns[0]
#             if len(columns) == 9:
#                 load = float(columns[-3].strip(","))
#             else:
#                 load = -1
#             if server not in history:
#                 history[server] = []
#             history[server].append(load)
#             if len(history[server]) > 60:
#                 del history[server][0]
#     with open(fn, "w") as f:
#         json.dump(history, f, indent=4)


# origins = [
#     "*",
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@api.get("/info")
async def load_info() -> str:
    return info()


def main():
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8086)) )


if __name__ == "__main__":
    main()
