# ================================
# GPU-enabled base image (Linux)
# ================================
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# ================================
# System dependencies
# ================================
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    curl \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Make python point to python3
RUN ln -s /usr/bin/python3 /usr/bin/python

# ================================
# Python tooling
# ================================
RUN pip install --upgrade pip

# ================================
# Deep Learning stack (GPU)
# ================================
# PyTorch with CUDA 12.1
RUN pip install \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu121

# NLP + Transformers + Data
RUN pip install \
    transformers \
    sentence-transformers \
    datasets \
    scikit-learn \
    pandas \
    numpy

# Backend (later use)
RUN pip install \
    fastapi \
    uvicorn

# ================================
# Workspace
# ================================
WORKDIR /workspace
