# UV 0.13.7-debian dev
FROM dhi.io/uv@sha256:68df03119a9e3a31c563c6afa398ed7b450dc5d8d12163f5ad44af715f893ca7 AS build

COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock
COPY uv.toml /app/uv.toml

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

RUN uv cache clean

WORKDIR /app

RUN uv sync --locked --no-build --no-dev --no-install-project --no-editable

COPY /src /app/src

RUN uv sync --locked --no-build --no-dev --no-editable

# Python 3.15.2-debian13
FROM dhi.io/python@sha256:a827761ad5c765368c5a31a67752b5b05846add889beceab18ddd7846ad20910 AS runtime

COPY --from=build --chown=65532:65532 /app/.venv /app/.venv

USER 65532
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/.venv/lib/python3.15/site-packages"
CMD ["python", "-m", "cerberus_backend.main"]

