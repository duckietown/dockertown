# Docker images

Don't use the constructor directly. Instead use 
```python
from dockertown import docker

my_docker_image = docker.image.inspect("my-image-name")

# or

my_docker_image = docker.pull("my-image-name")
```
For type hints, use this

```python
from dockertown import docker, Image

def print_dodo(image: Image):
    print(docker.run(image, ["echo", "dodo"]))
```


## Attributes

It attributes are the same that you get with the command line:
`docker image inspect ...`

To get a complete description of those attributes, you 
can take a look at the [daemon api reference page](https://docs.docker.com/engine/api/v1.40/#operation/ImageInspect) 
and click on "200 No error".

An example is worth many lines of descriptions.

```
In [1]: from dockertown import docker

In [2]: image = docker.pull("ubuntu")
20.04: Pulling from library/ubuntu
6a5697faee43: Pull complete
ba13d3bc422b: Pull complete
a254829d9e55: Pull complete
Digest: sha256:fff16eea1a8ae92867721d90c59a75652ea66d29c05294e6e2f898704bdb8cf1
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest

In [3]: def super_print(obj):
   ...:     print(f"type={type(obj)}, value={obj}")
   ...:

@INSERT_GENERATED_CODE@
```

## Methods

{{autogenerated}}
