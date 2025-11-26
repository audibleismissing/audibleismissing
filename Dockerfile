FROM python:3.14-slim-trixie

# Install uv.
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --from=ghcr.io/astral-sh/uv:0.9.12 /uv /uvx /bin/

# UV_COMPILE_BYTECODE=1 compiles Python bytecode for faster startup
# UV_LINK_MODE=copy ensures dependencies are copied (isolated env)
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen

# Copy the project into the image
ADD . /app
WORKDIR /app

# setup config directory
RUN mkdir /config

EXPOSE 8000

# Run for debugging 
# CMD ["tail", "-f", "/dev/null"]

# Run dev
CMD ["uv", "run", "fastapi", "run", "main.py", "--proxy-headers"]
# CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--host", "0.0.0.0"

# For prod, if running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0", "--proxy-headers"]
