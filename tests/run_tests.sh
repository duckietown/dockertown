set -e

# constants
SANDBOX_NAME=pydock-tests
SANDBOX_RUNTIME=docker.io/afdaniele/aavm-docker:20.10.7-amd64
SANDBOX_RUN="docker exec -it ${SANDBOX_NAME}"

# run a docker sandbox to run the tests in
docker run \
    -d \
    --rm \
    --name ${SANDBOX_NAME} \
    --tmpfs /tmp \
    --tmpfs /run \
    --tmpfs /run/lock \
    -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
    -v $(pwd):/workdir:ro \
    --workdir /workdir \
    -e DOCKER_CLI_EXPERIMENTAL=enabled \
    --privileged \
    ${SANDBOX_RUNTIME}

# wait until the sandbox is ready
while ! ${SANDBOX_RUN} docker ps
do
    echo waiting for sandbox...
    sleep 5
done

# - build an image containing the library inside the sandbox
${SANDBOX_RUN} docker buildx build --load -f tests/Dockerfile --target lint -t tests-image .

# - build an image containing the `tests_with_binaries` tests
${SANDBOX_RUN} docker buildx build --load -f tests/Dockerfile --target tests_with_binaries -t tests_with_binaries .
# - run the `tests_with_binaries` tests
${SANDBOX_RUN} docker run --rm -v /var/run/docker.sock:/var/run/docker.sock tests_with_binaries

# - build an image containing the `tests_without_any_binary` tests
${SANDBOX_RUN} docker buildx build --load -f tests/Dockerfile --target tests_without_any_binary -t tests_without_any_binary .
# - run the `tests_without_any_binary` tests
${SANDBOX_RUN} docker run --rm -v /var/run/docker.sock:/var/run/docker.sock tests_without_any_binary

# stop sandbox
docker stop ${SANDBOX_NAME}
