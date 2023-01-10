#/usr/bin/env python3
import os
import os.path
import re
import subprocess

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
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


def gpu_info():
    try:
        with subprocess.Popen(["nvidia-smi", "-L"], encoding="utf-8", stdout=subprocess.PIPE) as pipe:
            lines = pipe.stdout.readlines()
            return lines
    except:
        return []


def loadavg():
    with open("/proc/loadavg") as f:
        return float(f.readline().split()[0])


def info():
    output = get_spec()
    output["load"] = loadavg()
    output["ostype"] = ostype()
    output["gpu"] = gpu_info()
    return output



app = FastAPI()
api = FastAPI(root_path=f"/v{__api_version__}")
app.mount(f"/v{__api_version__}", api)



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
async def load_info():
    return info()
    return JSONResponse(content=info())


def main():
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8086)) )


if __name__ == "__main__":
    main()
