# 
This repository provides the code and experimental results associated with the paper **Embedding-Based Rankings of Educational Resources based on Learning Outcome Alignment: Benchmarking, Expert Validation, and Learner Performance**, which has been accepted for publication at **LAK 2026**.
## Setup

This project uses `uv` to manage the Python environment and dependencies. You can install `uv` by following the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/). Once `uv` is installed, you can synchronize the dependencies by running the following command in the project's root directory:

```bash
uv sync
```

> **Note:** If you prefer using `pip` to manage dependencies, a `requirements.txt` file is provided. However, it has not been tested and may not work as expected.

## Database Setup

To proceed, you need to download the database from [this link](https://2ly.link/27QHn) and extract it to date folder.

## Env setup

To set up the environment, run the following command:

```bash
cp .env_template .env
```

Then, open the `.env` file and fill in the required values.
## Usage
Create a new directory for the artifacts:
```bash
mkdir -p artifacts_paper
```

Then, run the following command to compute metrics:
```bash
# precision at 5
uv run cli.py metric precision-embedding  --at-n 5 -s db.sqlite3 -d artifacts_paper 
uv run cli.py metric precision-baseline  --at-n 5 -s db.sqlite3 -d artifacts_paper 
# precision at 3
uv run cli.py metric precision-embedding  --at-n 3 -s db.sqlite3 -d artifacts_paper 
uv run cli.py metric precision-baseline  --at-n 3 -s db.sqlite3 -d artifacts_paper 

# accuracy 
### Generating Embeddings
uv run cli.py metric acc-baseline --src-db db.sqlite3 -d artifacts_paper     
uv run cli.py metric acc-embedding --src-db db.sqlite3 -d artifacts_paper     

```
To generate embeddings, use the following command:

```bash
uv run cli.py dataops generate-synthetic-emb -s data/db.sqlite3  --embedding-model voyage/voyage-large-2-instruct --prompt-type lr-base-instruction --model-name openai/gpt-4o-mini  
```

You can also omit the `--model-name` parameter, and the script will compute embeddings for all remaining records matching the given prompt type.

### Evaluation

#### Computation of baseline and embeddings metrics

To compute the baseline and embeddings accuracy and precision metrics, use the following command:

```bash
uv run cli.py metric acc-baseline -s data/db.sqlite3 -d artifacts_paper
uv run cli.py metric acc-embedding -s data/db.sqlite3 -d artifacts_paper
uv run cli.py metric precision-baseline -s data/db.sqlite3 -d artifacts_paper
uv run cli.py metric precision-embedding -s data/db.sqlite3 -d artifacts_paper
```

For analysis of the generated results, refer to the `paper_result.ipynb` notebook.


