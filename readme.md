# Building a coding assistant with deeper understanding of a github repo Using WasmEdge

## Overview

This guide outlines the step-by-step process to set up a **cross-platform LLM runtime** using **WasmEdge**, create a **vector database** with **Qdrant**, and generate a knowledge base from a GitHub repository. Follow the steps below to configure your environment, fetch data, and generate an efficient knowledge base.

---

## Prerequisites

Ensure the following tools are installed on your system before proceeding:

1. **Docker**:  
   Install Docker using the [official Docker Engine installation guide](https://docs.docker.com/engine/install/ubuntu/) or the [Docker Desktop setup guide](https://docs.docker.com/desktop/setup/install/linux/).

2. **Python**: Version 3.6 or above.

---

## Steps

### **1. Install WasmEdge Runtime**
Install the WasmEdge Runtime, a lightweight and high-performance WebAssembly runtime for AI applications.  
Run the following command in your terminal:
```bash
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install_v2.sh | bash -s
```

---

### **2. Download the Embedding Model**
Download the required embedding model from Hugging Face:
```bash
curl -LO https://huggingface.co/gaianet/Nomic-embed-text-v1.5-Embedding-GGUF/resolve/main/nomic-embed-t
```

---

### **3. Start Qdrant Server**
Qdrant is a vector database that will store and retrieve embeddings. Use Docker to start the Qdrant server.

#### Create Storage and Snapshot Directories:
```bash
mkdir qdrant_storage
mkdir qdrant_snapshots
```

#### Run Qdrant Using Docker:
```bash
nohup docker run -d -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    -v $(pwd)/qdrant_snapshots:/qdrant/snapshots:z \
    qdrant/qdrant
```

#### **Note**:  
If Docker is not installed, follow these steps for Ubuntu 24.04:  
```bash
sudo apt remove docker-desktop
rm -r $HOME/.docker/desktop
sudo rm /usr/local/bin/com.docker.cli
sudo apt purge docker-desktop
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
sudo apt-get update
cd Downloads
sudo apt-get install ./docker.deb
systemctl --user restart docker-desktop
docker --version
```

These commands are also available in the `docker_init.sh` script.

---

### **4. Fetch Data from a GitHub Repository**
Use the provided Python scripts to extract markdown or Python files from a GitHub repository.  

#### Command for Markdown Files:
```bash
python md_file.py <repo_link> <path_to_output.csv>
```

#### Command for Python Files:
```bash
python python_file.py <repo_link> <path_to_output.csv>
```

These commands will generate a CSV file containing the file paths and their content.

---

### **5. Summarize Data and Generate QnA Pairs**
Run the following command to summarize repository content and generate Q&A pairs:
```bash
python summarizer.py <path_to_output.csv> <path_to_summary.csv>
```

#### **Note**:  
This step may take time depending on the size of your repository and the model used. The output CSV will contain two columns:  
- **Content**  
- **Summary and QnA Pairs**

---

### **6. Create a Knowledge Base**
Use the **GaiaNet embedding tools** to generate a knowledge base from the summary CSV file.

#### Steps:
1. **Download Required Files:**
   ```bash
   curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install_v2.sh | bash -s
   curl -LO https://huggingface.co/gaianet/Nomic-embed-text-v1.5-Embedding-GGUF/resolve/main/nomic-embed-text-v1.5.f16.gguf
   curl -LO https://github.com/GaiaNet-AI/embedding-tools/raw/main/csv_embed/csv_embed.wasm
   ```

2. **Delete Default Qdrant Collection:**
   ```bash
   curl -X DELETE 'http://localhost:6333/collections/default'
   ```

3. **Create a New Qdrant Collection:**
   ```bash
   curl -X PUT 'http://localhost:6333/collections/default' \
     -H 'Content-Type: application/json' \
     --data-raw '{
       "vectors": {
         "size": 768,
         "distance": "Cosine",
         "on_disk": true
       }
     }'
   ```

4. **Generate Knowledge Base:**
   ```bash
   wasmedge --dir .:. \
     --nn-preload embedding:GGML:AUTO:nomic-embed-text-v1.5.f16.gguf \
     csv_embed.wasm embedding default 768 output_summary.csv --ctx_size 8192
   ```

5. **Save a Qdrant Snapshot:**
   ```bash
   curl -X POST 'http://localhost:6333/collections/default/snapshots'
   ```

The snapshot file will be saved in the `qdrant_snapshots` directory.

#### **Optional**: Compress the Snapshot:
```bash
sudo tar cvzf <your_name>.tar.gz <your_file>.snapshot
```

---

### **7. Automate Updates to the Knowledge Base**
To keep your knowledge base up-to-date, modify the `automate.sh` script with the appropriate file paths.  

Set up a cron job to automate execution. For example, to run the update script at **12:00 midnight**:
```bash
crontab -e
```

Add the following line:
```bash
0 12 * * * /home/user/automate.sh >> /home/user/logfile.log 2>&1
```

Press `Ctrl+X`, then `Y`, and hit `Enter` to save.

---

- After creating the knowledge base it can be used with various [node-configs](https://docs.gaianet.ai/node-guide/customize) as an end to end chatbot or a drop in replacement to tools like [Cursor IDE](https://docs.gaianet.ai/user-guide/apps/cursor)

## Additional Resources

- [Docker Engine Installation Guide](https://docs.docker.com/engine/install/ubuntu/)  
- [Docker Desktop Setup](https://docs.docker.com/desktop/setup/install/linux/)  
- [GaiaNet Embedding Tools Documentation](https://docs.gaianet.ai/creator-guide/knowledge/csv)  
- [Gaianet Agent Frameworks and Apps](https://docs.gaianet.ai/category/agent-frameworks-and-apps)
- [Node Configs supported by Gaianet](https://github.com/GaiaNet-AI/node-configs)  
---

## Notes

- **Ensure Docker is running** before starting the Qdrant server.  
- The process may take time depending on your hardware and input size.  
- Use the provided `docker_init.sh` and `automate.sh` scripts for convenience.
- **Run all the scripts in the base directory (home/user) to avoid any error.**
--- 

