
-----

# Finacle Script Generation using a Fine-Tuned Language Model

This project fine-tunes a large language model (LLM) to generate custom "Finacle Script" code based on natural language prompts. It utilizes modern, memory-efficient training techniques like QLoRA to make it possible to train powerful code-specific models on consumer-grade hardware.

## Table of Contents

1.  [Prerequisites](https://www.google.com/search?q=%231-prerequisites)
2.  [Project Setup](https://www.google.com/search?q=%232-project-setup)
3.  [Preparing Training Data](https://www.google.com/search?q=%233-preparing-training-data)
4.  [The Fine-Tuning Process](https://www.google.com/search?q=%234-the-fine-tuning-process)
5.  [Generating Scripts (Inference)](https://www.google.com/search?q=%235-generating-scripts-inference)
6.  [Utility Scripts](https://www.google.com/search?q=%236-utility-scripts)

-----

## 1\. Prerequisites

### Hardware

  * **GPU:** An NVIDIA GPU with at least **8GB of VRAM** is required. The process was successfully tested on an NVIDIA 3070.
  * **CPU/RAM:** A modern multi-core CPU and at least 16GB of system RAM are recommended.

### Software

  * **Operating System:** Windows 10/11.
  * **Python:** **Python 3.11.x (64-bit)**. It is critical to use a version compatible with the latest PyTorch builds. Newer versions like Python 3.13 were found to be incompatible during testing.
  * **NVIDIA CUDA Toolkit:** The CUDA Toolkit is required for the GPU to work with PyTorch. The specific version should be compatible with the PyTorch installation command. For `cu126`, you can install any CUDA 12.x version (e.g., 12.1 or newer). You can download it from the [NVIDIA CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive).

-----

## 2\. Project Setup

Follow these steps to set up the project environment from scratch.

### Step 1: Create the Project Directory

Create a main folder for your project and navigate into it.

### Step 2: Create a Python Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

### Step 3: Install PyTorch with CUDA

Install the correct version of PyTorch that supports your CUDA installation. This step is critical and must be done before installing other packages. The command below is for a CUDA 12.x compatible build.

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

### Step 4: Install Remaining Dependencies
install all these packages using a single command:

```bash
pip install -r requirements.txt
```

-----

## 3\. Preparing Training Data

The model learns from a dataset of examples provided in `training_data.json`.

  * **Format:** The file is a JSON array of objects.
  * **Structure:** Each object must contain two keys:
      * `"prompt"`: A natural language instruction describing the task.
      * `"script"`: The corresponding, correct Finacle script code.

**Example Entry:**

```json
{
  "prompt": "Write a script that subtracts 5 from 20 and prints the result.",
  "script": "<--start\nsv_a = 20\nsv_b = 5\nsv_c = sv_a - sv_b\nprint(sv_c)\nend-->"
}
```

For best results, the dataset should contain at least 200 diverse and high-quality examples.

-----

## 4\. The Fine-Tuning Process

The `finetune_lora.py` script handles the training. It uses **QLoRA (4-bit Quantization + LoRA)** to efficiently fine-tune the large base model on your hardware.

### Running the Training

Once your `training_data.json` file is ready, execute the following command to start the fine-tuning process:

```bash
python finetune_lora.py
```

The script will load the base model, apply the LoRA adapters, and begin training. The final trained adapter will be saved to the `output_dir` specified in the script (e.g., `./qlora-finetuned-deepseek-7b`).

### Key Script: `finetune_lora.py`

This script is configured to use the `deepseek-ai/deepseek-coder-6.7b-instruct` model, which has shown excellent performance on this task. It is optimized to run on an 8GB GPU.

-----

## 5\. Generating Scripts (Inference)

After training, the `generate_lora_deepseek.py` script is used to interact with your fine-tuned model.

### Running the Generator

Execute the script from your terminal:

```bash
python generate_lora_deepseek.py
```

The script will load the base model and your trained LoRA adapter, then present you with an interactive prompt.

### How it Works

  * The script loads the model once.
  * It enters a loop, showing a `Your Prompt >` input line.
  * You can type any request and press Enter. The model will generate the Finacle script.
  * To end the session, type `exit` or `quit`.

### Key Script: `generate_lora_deepseek.py`

This script is pre-configured to load the correct QLoRA model and use the direct prompt format required for high-quality, raw code generation.

-----

## 6\. Utility Scripts

A helper script, `view_data.py`, is provided to parse the `training_data.json` file and generate a human-readable Markdown file (`readable_training_data.md`) for easy review of the dataset.