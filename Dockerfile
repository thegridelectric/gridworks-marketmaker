# syntax=docker/dockerfile:1
#
# The MarketMaker as a container. The build context is this checkout; the
# image has the locked environment and the gwmm entry point and nothing
# about where it runs. Identity (the g.node.gt file) and settings (GWMM_*)
# come from the run: mount the file and set GWMM_G_NODE_PATH to it.
#
#     podman build -t marketmaker .
#     podman run --rm --env-file .env \
#         -v ./g.node.gt.json:/mm/g.node.gt.json:ro,z \
#         -e GWMM_G_NODE_PATH=/mm/g.node.gt.json marketmaker

FROM docker.io/library/python:3.12-slim-bookworm AS build
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src/ src/
RUN uv sync --locked --no-dev && rm -rf /root/.cache/uv

FROM docker.io/library/python:3.12-slim-bookworm
WORKDIR /app
COPY --from=build /app /app
RUN groupadd --gid 1000 mm \
    && useradd --uid 1000 --gid 1000 --create-home mm
USER mm
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["gwmm"]
CMD ["rabbit"]
