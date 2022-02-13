# silero_docker

Create a network (for windows at least):

```docker network create ipc_network```
  
Build and run the server:

```
docker build -t silero .
docker run --rm --network=ipc_network --name tts_dns silero
```

Build and run the client:

```
docker build -t silero_client -f dockerfile.client .
docker run --rm --network=ipc_network silero_client
```
