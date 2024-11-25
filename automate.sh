#!/bin/bash

mkdir qdrant_storage
mkdir qdrant_snapshots

nohup docker run -d -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    -v $(pwd)/qdrant_snapshots:/qdrant/snapshots:z \
    qdrant/qdrant

source /home/aru/anaconda3/etc/profile.d/conda.sh
conda activate venv

GITHUB_REPO_URL="add_repo_link"
OUTPUT_CSV_PATH="add_path_to_output_csv" 
OUTPUT_SUMMARY_PATH="add_path_to_summary_csv" 

python /home/user/md_file.py "$GITHUB_REPO_URL" "$OUTPUT_CSV_PATH" #replace md_file.py with github_parser.py, python_file.py

python /home/user/summarizer.py "$OUTPUT_CSV_PATH" "$OUTPUT_SUMMARY_PATH"

source /home/user/anaconda3/etc/profile.d/conda.sh  #replace with path to venv
conda activate venv

curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install_v2.sh | bash -s

curl -LO https://huggingface.co/gaianet/Nomic-embed-text-v1.5-Embedding-GGUF/resolve/main/nomic-embed-text-v1.5.f16.gguf

curl -X DELETE 'http://localhost:6333/collections/default'

curl -X PUT 'http://localhost:6333/collections/default' \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "vectors": {
      "size": 768,
      "distance": "Cosine",
      "on_disk": true
    }
  }'

curl -LO https://github.com/GaiaNet-AI/embedding-tools/raw/main/csv_embed/csv_embed.wasm

wasmedge --dir .:. \
  --nn-preload embedding:GGML:AUTO:nomic-embed-text-v1.5.f16.gguf \
  csv_embed.wasm embedding default 768 test_summary.csv --ctx_size 8192

curl -X POST 'http://localhost:6333/collections/default/snapshots'

conda deactivate



