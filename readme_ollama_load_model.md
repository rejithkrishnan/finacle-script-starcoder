Of course. Here is the final, comprehensive `README.md` file.

This version has been updated to include a detailed **Troubleshooting Guide** that documents all the common issues we encountered—and their solutions—making it a complete reference for this project.

-----

# Finacle Script Generation using a Fine-Tuned Language Model

This project fine-tunes a large language model (LLM) to generate custom "Finacle Script" code and answer conceptual questions based on natural language prompts. It utilizes modern, memory-efficient training techniques like QLoRA to make it possible to train powerful code-specific models on consumer-grade hardware.

## Table of Contents

1.  [Prerequisites](https://www.google.com/search?q=%231-prerequisites)
2.  [Project Setup](https://www.google.com/search?q=%232-project-setup)
3.  [The Fine-Tuning Process](https://www.google.com/search?q=%233-the-fine-tuning-process)
4.  [Interacting with the Model](https://www.google.com/search?q=%234-interacting-with-the-model)
5.  [Importing to Ollama](https://www.google.com/search?q=%235-importing-to-ollama)
6.  [Troubleshooting Guide](https://www.google.com/search?q=%236-troubleshooting-guide)

-----

## 1\. Prerequisites

### Hardware

  * **GPU:** An NVIDIA GPU with at least **8GB of VRAM** is required. The process was successfully tested on an NVIDIA 3070.
  * **CPU/RAM:** A modern multi-core CPU and at least 16GB of system RAM are recommended.

### Software

  * **Operating System:** Windows 10/11.
  * **Python:** **Python 3.11.x (64-bit)**. It is critical to use this version. Newer versions like Python 3.13 were found to be incompatible with the build dependencies of key packages like `sentencepiece`.
  * **NVIDIA CUDA Toolkit:** The CUDA Toolkit is required for the GPU to work with PyTorch. A version compatible with the PyTorch installation command is needed (e.g., CUDA 12.1 or newer for `cu12x` builds). You can download it from the [NVIDIA CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive).
  * **C++ Build Tools:** Required for compiling some Python packages from source.
  * **CMake:** Another build tool required for compiling the `sentencepiece` library.

-----

## 2\. Project Setup

Follow these steps to set up the project environment from scratch.

### Step 1: Create the Project Directory

Create a main folder for your project and navigate into it.

### Step 2: Install Build Tools

Before installing Python packages, ensure your system has the necessary compilers.

1.  **Install C++ Build Tools:**
      * Download the **Visual Studio Build Tools** installer from [visualstudio.microsoft.com/visual-cpp-build-tools/](https://www.google.com/search?q=https://visualstudio.microsoft.com/visual-cpp-build-tools/).
      * Run the installer and on the "Workloads" tab, select **"Desktop development with C++"**.
2.  **Install CMake:**
      * Download the "Windows x64 Installer" from [cmake.org/download/](https://cmake.org/download/).
      * Run the installer and, crucially, select the option **"Add CMake to the system PATH for all users"**.

### Step 3: Create a Python Virtual Environment

It is highly recommended to use a virtual environment linked to your Python 3.11 installation.

```bash
# Create the virtual environment using Python 3.11
py -3.11 -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

### Step 4: Install Dependencies via `requirements.txt`

Create a file named `requirements.txt` in your project folder with the following content.

#### `requirements.txt`

```
# Core ML Libraries
torch
torchvision
torchaudio
transformers
peft
bitsandbytes
accelerate
datasets

# Utility and Interaction
notebook
matplotlib
pandas
seaborn
Flask
requests
PyYAML
```

Now, install all these packages using a single command. The PyTorch version will be determined by your CUDA setup.

```bash
# For a CUDA 12.x setup
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Install all other packages
pip install -r requirements.txt
```

-----

## 3\. The Fine-Tuning Process

The `finetune_lora.py` script handles the training. It uses **QLoRA (4-bit Quantization + LoRA)** to efficiently fine-tune the large base model on your hardware.

### Data Preparation

  * Create a directory named `training_data`.
  * Inside this directory, place your training files in **JSON format**. The script is designed to load all `.json` files from this folder.
  * We recommend managing your data in the human-readable `editable_data.yml` file and using the provided `yaml_to_json.py` utility to generate the final `training_data.json` before training.

### Running the Training

Once your `training_data/` directory is populated, execute the following command:

```bash
python finetune_lora.py
```

The script will load the base model (`deepseek-ai/deepseek-coder-6.7b-instruct`), apply the LoRA adapters, and begin training. The final trained adapter will be saved to the `output_dir` specified in the script (e.g., `./qlora-finetuned-deepseek-7b`).

-----

## 4\. Interacting with the Model

After training, the `generate_lora_deepseek.py` script is used to interact with your fine-tuned model via a command-line chat interface.

### Running the Generator

Execute the script from your terminal:

```bash
python generate_lora_deepseek.py
```

The script loads the model and then presents an interactive prompt. You can ask conceptual questions or give it commands to generate scripts. To end the session, type `exit` or `quit`.

-----

## 5\. Importing to Ollama

To create a portable version of your model, you can import it into Ollama.

### Step 1: Merge the LoRA Adapter

Run the `merge_lora.py` script to combine your fine-tuned adapter with the base model. This creates a complete, standalone model in the `./merged-finacle-model` directory.

```bash
python merge_lora.py
```

### Step 2: Convert to GGUF Format

Use the conversion script from the `llama.cpp` repository to convert the merged model into a quantized GGUF file.

```bash
python ../llama.cpp/convert_hf_to_gguf.py ./merged-finacle-model --outtype q8_0 --outfile finacle-coder.gguf
```

### Step 3: Create an Ollama `Modelfile`

Create a `Modelfile` (no extension) in your project directory to configure how Ollama should run your model.

### Step 4: Import and Run

Use the `ollama` commands to create and run your custom model.

```bash
# Create the model in Ollama's registry
ollama create my-finacle-assistant -f Modelfile

# Run your model
ollama run my-finacle-assistant
```

-----

## 6\. Troubleshooting Guide

This section covers the common errors encountered during this project and their solutions.

  * **Build Error for `numpy` or `sentencepiece`:**

      * **Error:** `ERROR: Could not find a version that satisfies the requirement...` or `subprocess-exited-with-error`.
      * **Cause:** This happens when `pip` cannot find a pre-compiled version (a `.whl` file) for your Python version and tries to build the package from source. This build process requires C++ compilers and CMake.
      * **Solution:**
        1.  Ensure you have installed the **Visual Studio C++ Build Tools** and **CMake** as described in the setup section.
        2.  **The most reliable fix is to use Python 3.11**. These libraries have pre-compiled versions for Python 3.11, which avoids the need for local compilation entirely.

  * **Memory Error During Model Merging:**

      * **Error:** `ValueError: We need an 'offload_dir' to dispatch this model...`
      * **Cause:** Your GPU does not have enough VRAM to hold the entire base model and the LoRA adapter simultaneously during the merge process.
      * **Solution:** Modify your `merge_lora.py` script to specify a temporary disk offload directory.
        ```python
        import os
        offload_dir = "./offload"
        os.makedirs(offload_dir, exist_ok=True)
        # ...
        model = PeftModel.from_pretrained(base_model, adapter_path, offload_folder=offload_dir)
        ```

  * **`convert.py` Not Found Error:**

      * **Error:** `[Errno 2] No such file or directory: 'llama.cpp\\convert.py'`
      * **Cause:** The `llama.cpp` repository has been updated, and the main conversion script has been renamed.
      * **Solution:** Use the new, correct script name in your command: **`convert_hf_to_gguf.py`**.

  * **Invalid Quantization Type Error:**

      * **Error:** `argument --outtype: invalid choice: 'q4_K_M'`
      * **Cause:** The Python conversion script (`convert_hf_to_gguf.py`) has limited quantization capabilities and does not support advanced types like `q4_K_M`.
      * **Solution:** Use a supported quantization type. **`q8_0`** is the recommended choice for a good balance of quality and performance.
        ```bash
        # Corrected command
        python ../llama.cpp/convert_hf_to_gguf.py ./merged-finacle-model --outtype q8_0 --outfile finacle-coder.gguf
        ```