FROM busybox as get_buildx

RUN wget -O /docker-buildx https://github.com/docker/buildx/releases/download/v0.6.0/buildx-v0.6.0.linux-amd64
RUN chmod a+x /docker-buildx


#-----------------------------------------------------------------------------
FROM busybox as get_compose

RUN wget -O /docker-compose https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64
RUN chmod a+x /docker-compose


#-----------------------------------------------------------------------------
FROM python:3.7 as python_dependencies

RUN pip install pydantic requests tqdm flake8 isort black

COPY tests/test-requirements.txt /tmp/
COPY requirements.txt /tmp/
RUN pip install -r /tmp/test-requirements.txt -r /tmp/requirements.txt


#-----------------------------------------------------------------------------
FROM python_dependencies as lint
WORKDIR /dockertown
COPY . .
RUN flake8
RUN isort --check ./
RUN black --check ./


#-----------------------------------------------------------------------------
FROM python_dependencies as tests_with_binaries
COPY --from=docker:20.10 /usr/local/bin/docker /usr/bin/
COPY --from=get_buildx /docker-buildx /root/.docker/cli-plugins/
COPY --from=get_compose /docker-compose /root/.docker/cli-plugins/

WORKDIR /dockertown
ENV HOME=/root

COPY . .

RUN pip install -e .

CMD pytest -v --durations=10 ./tests


#-----------------------------------------------------------------------------
FROM python_dependencies as tests_without_any_binary

COPY --from=get_buildx /docker-buildx /root/.docker/cli-plugins/

WORKDIR /dockertown
COPY . .

RUN pip install -e .

CMD pytest -v --durations=10 ./tests/dockertown/components/buildx
