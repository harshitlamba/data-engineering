FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# we don't need this as we use uv with the required dependencies
# RUN pip install pandas pyarrow

WORKDIR /code
# a way to execute the command without uv run in the entrypoint is to set the bin
# path in environment variables of the container
ENV PATH="/code/.venv/bin:$PATH"

# we have some uv files in our pipeline folder that contains the required config
# hence, we move to the directory inside container where the pipeline code would be stored
# to copy all the uv files
COPY .python-version pyproject.toml uv.lock ./
# create the environment and install the dependencies from the lock file
RUN uv sync --locked

# copy the pipeline logic at in the code directory inside container
COPY pipeline.py .

# execute the command to run pipeline.py; it will directly execute the script without 
# manually running from bash
# ENTRYPOINT ["uv", "run", "python", "pipeline.py"]
ENTRYPOINT ["python", "pipeline.py"]
