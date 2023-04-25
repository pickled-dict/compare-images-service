import os
import sys
import json
import time
import docker
from dotenv import dotenv_values


env = dotenv_values('.env')
docker_client = docker.from_env()

CONTAINER_NAME          = env['CONTAINER_NAME']
DATABASE_URL            = env['DATABASE_URL'] 
NEXTAUTH_URL            = env['NEXTAUTH_URL']
GITHUB_CLIENT_ID        = env['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET    = env['GITHUB_CLIENT_SECRET']
NEXTAUTH_SECRET         = env['NEXTAUTH_SECRET']
IMAGE_NAME              = env['IMAGE_NAME'] 

DOCKER_RUN_CMD = """docker run -p 3000:3000 --name {0} \\
-e DATABASE_URL="{1}" \\
-e NEXTAUTH_URL="{2}" \\
-e GITHUB_CLIENT_ID="{3}" \\
-e GITHUB_CLIENT_SECRET="{4}" \\
-e NEXTAUTH_SECRET="{5}" \\
-d {6}
""".format(
    CONTAINER_NAME,
    DATABASE_URL,
    NEXTAUTH_URL,
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    NEXTAUTH_SECRET,
    IMAGE_NAME
)


def log(s: str):
    print(s)
    sys.stdout.flush()


# check docker client to see if image with image name exists
try:
    docker_client.images.get(IMAGE_NAME)
    log(f'Image with name {IMAGE_NAME} exists')
except:
    log(f'Image with name {IMAGE_NAME} was not found')
    os.system(f'docker pull {IMAGE_NAME}')
    log('Image pulled from Dockerhub')

# check docker client to see if container exists -- if not, 
# start, if exists but is stopped, start stopped container
try:
    container = docker_client.containers.get(CONTAINER_NAME)
    if container.attrs['State']['Running'] == False:
        log(f'Container with name {CONTAINER_NAME} is not currently running')
        os.system(f'docker container start {CONTAINER_NAME}')
        log('Stopped container has been restarted')
except:
    log('Docker container not found, starting a fresh container')
    os.system(DOCKER_RUN_CMD)
    log('Fresh container started')


# main loop that checks if the current image matches the remote one
while True:
    old = json.loads(os.popen(f'docker image inspect {IMAGE_NAME}').read())[0]['Id']
    os.system(f'docker pull {IMAGE_NAME}')
    new = json.loads(os.popen(f'docker image inspect {IMAGE_NAME}').read())[0]['Id']

    equal = old == new

    print(old)
    print(new)
    print(f"equal?: {equal}")
    sys.stdout.flush()

    if not equal:
        os.system(f'docker container stop {CONTAINER_NAME}')
        os.system(f'docker container rm {CONTAINER_NAME}')
        os.system(DOCKER_RUN_CMD)

    time.sleep(10)

