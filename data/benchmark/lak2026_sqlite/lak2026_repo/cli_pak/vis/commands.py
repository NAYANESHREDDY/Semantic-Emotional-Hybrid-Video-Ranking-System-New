from datetime import datetime
from pathlib import Path

import click
import pandas as pd
from loguru import logger
from tabulate import tabulate
from tqdm import tqdm

from const import providers
from db_ops import get_db_connection


def generate_expr_dest_root(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    # get all current subdirectories
    subdirs = [d for d in root.iterdir() if d.is_dir()]
    prefix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dest_root = root / f"{len(subdirs) + 1}-{prefix}"
    dest_root.mkdir(parents=True, exist_ok=True)
    return dest_root


@click.group()
def vis():
    pass


@vis.command("prompt-type-model-count")
@click.option("-s", "--src-db-path", type=str, required=True)
def prompt_type_count(src_db_path: str):
    conn = get_db_connection(src_db_path)
    get_query = """SELECT model_name,type,COUNT(*)
FROM SyntaticData
JOIN Prompt p ON p.id = SyntaticData.prompt_id
GROUP BY model_name,type;
"""
    df = pd.read_sql_query(get_query, conn)
    # update the tabulate to show row numbers
    df.index = df.index + 1
    print(tabulate(df, headers="keys", showindex=True, tablefmt="fancy_grid"))


@vis.command("embedding-stats")
@click.option("-s", "--src-db-path", type=str, required=True)
@click.option("--show-missing", is_flag=True, default=False)
def embedding_stats(src_db_path: str, show_missing: bool):
    conn = get_db_connection(src_db_path)
    query = """SELECT sd.extracted_content, sd.id as sd_id, sdev.value, p.type,sd.model_name, sdev.which
    FROM SyntaticData sd
    JOIN Prompt p ON sd.prompt_id = p.id
    LEFT JOIN SyntacticDataEmbeddingVector sdev 
        ON sd.id = sdev.syntactic_data_id 
    WHERE sd.extracted_content IS NOT NULL
        """
    df = pd.read_sql_query(query, conn)
    df = (
        df.groupby(["model_name", "type"])
        .agg(
            total_rows=("value", "count"),
            has_embedding=("value", lambda x: x.notna().sum()),
            missing_embedding=("value", lambda x: x.isna().sum()),
        )
        .reset_index()
    )
    if show_missing:
        df = df[df["missing_embedding"] > 0]

    print(tabulate(df, headers="keys", showindex=True, tablefmt="fancy_grid"))


def generate_comparison_markdown(data, title,n_samples=None):
    markdown_output = []
    n_records = data.shape[0] if n_samples is None else n_samples
    pbar = tqdm(range(n_records), desc="Processing", unit="item", colour="green")

    for index, ((prompt_id, context_id), group) in enumerate(data.iterrows()):
        prompt_text = group.prompt_text.iloc[0]
        markdown_output.append(f"## Sample {index + 1}\n")
        markdown_output.append(f"### Prompt {prompt_id}\n")
        markdown_output.append(f"**Context** : {context_id}\n")
        markdown_output.append(f"{prompt_text}\n\n")

        markdown_output.append("| Model | Content |")
        markdown_output.append("|-------|---------|")

        for model_name, generated_content in group.content.items():
            try:
                clean_content = generated_content.replace("\n", " ").replace("|", "\\|")
            except:
                clean_content = generated_content
            markdown_output.append(f"| {model_name} | {clean_content} |")
        pbar.update(1)

        # Add spacing between prompts
        markdown_output.append("\n\n")
        markdown_output.append("--------------------------------")
        if n_samples is not None and index >= n_samples:
            break
    pbar.close()
    markdown_output.insert(0, f"# Expr : {title}\n")
    return "\n".join(markdown_output)


@vis.command("data-sample")
@click.option("-s", "--src-db-path", type=str, required=True)
@click.option(
    "--model-name", type=click.Choice(providers), required=False, default=None
)
@click.option(
    "--prompt-type",
    type=click.Choice(
        ["without_cognitive_impairment", "with_cognitive_impairment", "long", "short"]
    ),
    required=True,
    default="long",
)
@click.option("-n", "--n-samples", type=int, required=False, default=None)
@click.option("-o", "--output-dir", type=str, required=False, default="artifacts")
@click.option("--new-dir", is_flag=True, default=False)
def data_sample(
    src_db_path: str, model_name: str, prompt_type: str, n_samples: int, output_dir: str,new_dir:bool
):
    conn = get_db_connection(src_db_path)

    query = """SELECT sd.extracted_content,sd.model_name, sd.id, p.id as prompt_id, p.type,p.text,p.context_resource_id,sdev.which, R.url,R.content
    FROM SyntaticData sd
    JOIN Prompt p ON sd.prompt_id = p.id
    LEFT JOIN SyntacticDataEmbeddingVector sdev 
        ON sd.id = sdev.syntactic_data_id 
    JOIN Resources R ON p.context_resource_id = R.id
    WHERE (? is NULL OR sd.model_name = ?)
        AND sd.extracted_content IS NOT NULL
        AND p.type = ?

"""

    df = pd.read_sql_query(
        query, conn, params=(model_name, model_name, prompt_type)
    )
    res = df.groupby(["prompt_id", "context_resource_id", "model_name"]).agg(
        content=("extracted_content", "first"),
        prompt_text=("text", "first"),
    )
    t = res.unstack(level="model_name")
    markdown_text = generate_comparison_markdown(
        t, f"Model : {model_name or 'All'} Prompt Type : {prompt_type}",n_samples=n_samples
    )
    if new_dir:
        dest_root = generate_expr_dest_root(Path(output_dir))
    else:
        dest_root = Path(output_dir)
    with open(dest_root / "comparison.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)
    res.to_excel(dest_root / "comparison.xlsx", index=False)
    logger.info(f"Saved to {dest_root}")

