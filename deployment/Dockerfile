FROM python:3.10-slim as builder

# Define build arguments
ARG GIT_ACCESS_TOKEN=
ENV GITHUB_ACCESS_TOKEN=$GIT_ACCESS_TOKEN

# Install git
RUN apt-get update
RUN apt-get install -y git

# Copy package
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
WORKDIR /app

# Install package and dependencies
RUN echo "https://${GITHUB_ACCESS_TOKEN}:@github.com" > ~/.git-credentials
RUN git config --global credential.helper store
RUN pip install --upgrade pip
RUN pip install --user -e .
RUN rm -f ~/.git-credentials

# Uncomment to keep container alive
# CMD tail -f /dev/null

# Build final image
FROM python:3.10-slim as release

# Copy in dependencies
COPY --from=builder /root/.local /root/.local
ENV PATH="/root/.local:$PATH"

# Copy package
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
WORKDIR /app

# Install package
RUN pip install --upgrade pip
RUN pip install -e . --no-deps

# Uncomment to keep container alive
# CMD tail -f /dev/null