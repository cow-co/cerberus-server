# UV 0.13.7-debian dev
FROM dhi.io/uv@sha256:68df03119a9e3a31c563c6afa398ed7b450dc5d8d12163f5ad44af715f893ca7 AS build

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock
COPY ./src /app/src
RUN uv sync

# Python 3.14.10-debian13
FROM dhi.io/python@sha256:8e34f57c013710aff00f29d8c7003a47abe39971c8c8d94b61cf144737b356a0 AS runtime

COPY --from=build --chown=65532:65532 /app/.venv /app/.venv

USER 65532
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/.venv/lib/python3.14/site-packages"
CMD ["python", "-m", "cerberus_backend.main"]

