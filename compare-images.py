import os
import json
import time

DOCKER_RUN_CMD = """docker run -p 3000:3000 --name <REPLACE ME> \\
-e DATABASE_URL=<REPLACE ME> \\
-e NEXTAUTH_URL="<REPLACE ME>" \\
-e GITHUB_CLIENT_SECRET="<REPLACE ME>" \\
-e NEXTAUTH_SECRET="<REPLACE ME>" \\
-d <REPLACE ME>"""

def log_it(s: str):
    print(f"{time.ctime()}: {s}")

while True:
    old = json.loads(os.popen('docker image inspect <REPLACE ME>').read())[0]['Id']
    os.system('docker pull <REPLACE ME>')
    new = json.loads(os.popen('docker image inspect <REPLACE ME>').read())[0]['Id']

    equal = old == new

    log_it(old)
    log_it(new)
    log_it(f"are they equal?: {equal}")

    if not equal:
        os.system('docker container stop <REPLACE ME>')
        os.system('docker container rm <REPLACE ME>')
        os.system(DOCKER_RUN_CMD)

    time.sleep(10)

