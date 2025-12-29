## Docext Server Install Guide (Docker and Python)

This guide is a reusable checklist for deploying Docext on a Linux server.

### Prerequisites
- Ubuntu 22.04+ (or similar)
- NVIDIA GPU with CUDA drivers installed
- Open TCP port 7860 (default UI/API port)
- Hugging Face token with read access (recommended)

Set the token in your shell:
```
export HUGGING_FACE_HUB_TOKEN=hf_...
```

## Option A: Docker (recommended)

### 1) Install Docker
```
apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 2) Install NVIDIA Container Toolkit
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | gpg --dearmor -o /etc/apt/keyrings/nvidia-container-toolkit.gpg
curl -fsSL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/etc/apt/keyrings/nvidia-container-toolkit.gpg] https://#g' \
  > /etc/apt/sources.list.d/nvidia-container-toolkit.list

apt-get update
apt-get install -y nvidia-container-toolkit
nvidia-ctk runtime configure --runtime=docker
systemctl restart docker
```

### 3) Run Docext
```
docker run --rm \
  --env "HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN" \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --network host \
  --shm-size=20.24gb \
  --gpus all \
  nanonetsopensource/docext:v0.1.10 \
  --model_name "hosted_vllm/nanonets/Nanonets-OCR-s"
```

### 4) Access
- UI and API: `http://<server-host>:7860`
- Login: `admin` / `admin`

## Option B: Python (no Docker)

### 1) Install system deps
```
apt-get update
apt-get install -y git python3.11 python3.11-venv poppler-utils
```

### 2) Install Docext
```
git clone https://github.com/nanonets/docext.git
cd docext
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

### 3) Run Docext
```
python -m docext.app.app --model_name hosted_vllm/nanonets/Nanonets-OCR-s
```

### 4) Access
- UI and API: `http://<server-host>:7860`
- Login: `admin` / `admin`

## Notes
- If PDF uploads fail with `pdfinfo` errors, install `poppler-utils`.
- If running inside a containerized host without systemd, you may need to start Docker manually:
  `dockerd --iptables=false --ip-forward=false --ip-masq=false --bridge=none &`
