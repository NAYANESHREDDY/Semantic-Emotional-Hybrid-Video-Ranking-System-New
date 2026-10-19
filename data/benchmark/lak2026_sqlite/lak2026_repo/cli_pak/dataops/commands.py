import asyncio
import datetime
import json
import os
import timeit
from pathlib import Path

import click
import pandas as pd
from loguru import logger
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer
from const import (
    PROMPT_COG_LR_BASES_INSTRUCTION,
    PROMPT_LR_BASE_BRIEF,
    PROMPT_WITH_COGNITIVE_IMPAIRMENT,
    PROMPT_WITHOUT_COGNITIVE_IMPAIRMENT,
    providers,
)
from db_ops import (
    ReducingStrategy,
    get_db_connection,
    get_resource_id_given_url,
    get_syntactic_data,
    get_topic_given_res_id,
    insert_syntactic_data_embedding,
)
from embeddings_ops import (
    batch_get_embeddings,
    get_len_safe_bert_embedding,
    len_safe_get_embedding,
)
from llm_ops import process_synthetic_prompts


@click.group()
def dataops():
    pass


@dataops.command("allm-prompt-response")
@click.option(
    "-s",
    "--src-db",
    required=True,
    type=click.Path(),
    help="input db file, raw data from edoer",
)
@click.option(
    "--model",
    required=True,
    default="openai/gpt-4o",
    type=click.Choice(providers),
    help="LLM model provide name to use",
)
@click.option("--temperature", type=float, default=0.0, help="temperature")
@click.option(
    "--max-concurrent-requests", type=int, default=5, help="max_concurrent_requests"
)
@click.option(
    "--system-prompt",
    type=str,
    default="You are a helpful assistant to generate education content.",
    help="system prompt",
)
@click.option(
    "--prompt-type",
    type=click.Choice(
        [
            "cognitive_impairment",
            "without_cognitive_impairment",
            "long",
            "short",
            "lr-base-instruction",
            "lr-base-brief",
        ]
    ),
    default="cognitive_impairment",
    help="prompt type",
)
def allm_prompt_response(
    src_db, model, temperature, max_concurrent_requests, system_prompt, prompt_type
):
    start = timeit.default_timer()
    asyncio.run(
        process_synthetic_prompts(
            src_db,
            model,
            prompt_type,
            temperature,
            system_prompt,
            max_concurrent_requests,
        )
    )
    end = timeit.default_timer()
    elapsed = end - start
    # convert to HH:MM:SS using datetime
    elapsed_str = datetime.timedelta(seconds=elapsed)
    logger.info(f"allm prompt response: Time taken: {elapsed_str}")


def one_vs_rest_combinations(group):
    resource_ids = group["resource_id"].tolist()
    contents = group["content"].tolist()
    n_tokens = group["n_tokens"].tolist()
    topic_id = set(group["topic_id"])
    assert len(topic_id) == 1
    topic_id = topic_id.pop()
    combinations = []
    for i, (resource_id, content, n_token) in enumerate(
        zip(resource_ids, contents, n_tokens)
    ):
        rest_ids = resource_ids[:i] + resource_ids[i + 1 :]
        combinations.append((topic_id, resource_id, rest_ids, content))
    return pd.DataFrame(
        combinations, columns=["topic_id", "context_resource_id", "rest", "context"]
    )


@dataops.command(
    "create-prompt",
    help="Create prompts for the given prompt type, it follows one vs rest for the example substitutions",
)
@click.option(
    "-s",
    "--src-db",
    required=True,
    type=click.Path(),
    help="input db file, raw data from edoer",
)
@click.option(
    "--prompt-type",
    type=click.Choice(["cognitive_impairment", "without_cognitive_impairment"]),
    default="cognitive_impairment",
    help="prompt type",
)
def create_prompt(src_db, prompt_type):
    get_query = """ SELECT T.title, TRL.topic_id, TRL.status,TRL.resource_id, R.content,R.n_tokens FROM Topics T 
    JOIN TopicResourceLink TRL on TRL.topic_id = T.id
    JOIN Resources R on R.id = TRL.resource_id
    WHERE R.content IS NOT NULL AND TRL.status = 'Accepted' ;
    """

    conn = get_db_connection(src_db, auto_commit=True)
    df = pd.read_sql_query(get_query, conn)
    pairs_all_content = (
        df.groupby("title")
        .apply(one_vs_rest_combinations)
        .reset_index(level=1, drop=True)
        .reset_index()
    )
    match prompt_type:
        case "cognitive_impairment":
            prompt = PROMPT_WITH_COGNITIVE_IMPAIRMENT
        case "without_cognitive_impairment":
            prompt = PROMPT_WITHOUT_COGNITIVE_IMPAIRMENT
        case _:
            raise ValueError(f"Invalid prompt type: {prompt_type}")
    prompts = []
    cur = conn.cursor()
    pbar = tqdm(total=len(pairs_all_content), colour="green")
    for _, row in pairs_all_content.iterrows():
        topic_id = row["topic_id"]
        resource_id = row["context_resource_id"]
        rest = row["rest"]
        context = row["context"]
        prompt_filled_in = prompt.format(
            TOPIC_TITLE=row["title"], EXAMPLE_CONTENT="".join(context)
        )
        prompts.append((topic_id, resource_id, rest, prompt_filled_in))
        insert_query = """
        INSERT INTO Prompt (topic_id, context_resource_id, text, type) VALUES (?, ?, ?, ?)
        """
        cur.execute(
            insert_query,
            (topic_id, resource_id, prompt_filled_in, prompt_type),
        )
        conn.commit()
        pbar.update(1)
    pbar.close()
    conn.close()
    logger.info(
        f"Prompt generation completed for {prompt_type} with {len(prompts)} prompts"
    )


@dataops.command("create-lr-base-prompt")
@click.option("-s", "--src-db", type=str, default="./db.sqlite3", help="source db")
@click.option(
    "--input-file",
    type=str,
    required=True,
    help="input file contains ths topics with their learning outcomes",
)
@click.option(
    "--lr-column-name",
    type=str,
    required=True,
    help="column name of the learning outcomes",
)
@click.option(
    "--prompt-type",
    type=click.Choice(["lr-base-instruction", "lr-base-brief"]),
    default="lr-base-instruction",
    help="prompt type to be used",
)
def create_lr_base_prompt(src_db, input_file, lr_column_name, prompt_type):
    input_file = Path(input_file)
    assert (
        input_file.exists() and input_file.is_file() and input_file.suffix == ".csv"
    ), "input file must be a csv file"
    df = pd.read_csv(input_file, header=0)
    assert lr_column_name in df.columns, (
        f"learning outcome column {lr_column_name} not found in the input file"
    )
    match prompt_type:
        case "lr-base-instruction":
            prompt = PROMPT_COG_LR_BASES_INSTRUCTION
        case "lr-base-brief":
            prompt = PROMPT_LR_BASE_BRIEF
        case _:
            raise ValueError(f"Invalid prompt type: {prompt_type}")
    conn = get_db_connection(src_db, auto_commit=True)
    cur = conn.cursor()
    pbar = tqdm(total=len(df), colour="green")
    for _, row in df.iterrows():
        url = row["url"]
        topic_title = row["title"]
        res_id = get_resource_id_given_url(url, conn)
        topic_id = get_topic_given_res_id(res_id, conn)
        learning_outcomes = row[lr_column_name]
        prompt_filled_in = prompt.format(
            TOPIC_TITLE=topic_title, LEARNING_OUTCOMES=learning_outcomes
        )
        insert_query = """
        INSERT INTO Prompt (topic_id, context_resource_id, text, type) VALUES (?, ?, ?, ?)
        """
        cur.execute(
            insert_query,
            (topic_id, res_id, prompt_filled_in, prompt_type),
        )
        conn.commit()
        pbar.update(1)
    pbar.close()
    conn.close()
    logger.info(f"Prompt generation completed for {prompt_type} with {len(df)} prompts")


@dataops.command("generate-synthetic-emb")
@click.option("-s", "--src-db", type=str, default="./db.sqlite3", help="source db")
@click.option(
    "--model-name",
    type=click.Choice(providers),
    default=None,
    required=False,
    help="model name",
)
@click.option(
    "--prompt-type",
    type=click.Choice(
        [
            "without_cognitive_impairment",
            "long",
            "short",
            "cognitive_impairment",
            "lr-base-instruction",
            "lr-base-brief",
        ]
    ),
    default="without_cognitive_impairment",
    help="prompt type",
)
@click.option(
    "--embedding-model",
    type=click.Choice(["voyage/voyage-large-2-instruct", "voyage/voyage-3"]),
    default="voyage/voyage-large-2-instruct",
)
@click.option(
    "--tokenization-alg",
    type=click.Choice(["voyageai/voyage"]),
    default="voyageai/voyage",
    help="tokenization algorithm",
)
@click.option(
    "--reduce-strategy",
    type=click.Choice([m.value for m in ReducingStrategy]),
    default="average",
    help="reducing strategy",
)
@click.option(
    "--max-tokens",
    type=int,
    default=16000,
    help="max tokens",
)
def create_syntatic_data_embeddings(
    src_db,
    model_name,
    prompt_type,
    embedding_model,
    tokenization_alg,
    reduce_strategy,
    max_tokens,
):
    assert os.getenv("VOYAGE_API_KEY") is not None, "VOYAGE_API_KEY is not set"
    conn = get_db_connection(src_db, auto_commit=True)
    reduce_strategy = ReducingStrategy(reduce_strategy)
    embeddings = get_syntactic_data(
        conn,
        model_name,
        prompt_type,
        embedding_model,
        tokenization_alg,
        reduce_strategy,
    )
    errors = []
    logger.debug(f"found {len(embeddings)} embeddings to generate")
    # exit()
    pbar = tqdm(total=len(embeddings), colour="green")
    for s_text, s_id in embeddings:
        try:
            embedding, usage = len_safe_get_embedding(
                s_text, embedding_model, max_tokens, tokenization_alg, reduce_strategy
            )

            embedding_json = json.dumps(embedding)

            insert_syntactic_data_embedding(
                conn,
                s_id,
                embedding_model,
                tokenization_alg,
                reduce_strategy,
                embedding_json,
                usage,
            )

        except Exception as e:
            errors.append((s_id, e))
            logger.info(f"Errors: {errors}")
        pbar.update(1)
    pbar.close()
    conn.close()
    if len(errors) > 0:
        # write to json
        logger.warning(f"Errors: {errors}")

        with open("errors.json", "w") as f:
            json.dump(errors, f)
    else:
        logger.info("No errors")


@dataops.command("agenerate-synthetic-emb")
@click.option("-s", "--src-db", type=str, default="./db.sqlite3", help="source db")
@click.option(
    "--model-name",
    type=click.Choice(providers),
    default=None,
    required=False,
    help="model name",
)
@click.option(
    "--prompt-type",
    type=click.Choice(
        ["without_cognitive_impairment", "long", "short", "cognitive_impairment"]
    ),
    default="without_cognitive_impairment",
    help="prompt type",
)
@click.option(
    "--embedding-model",
    type=click.Choice(["voyage/voyage-large-2-instruct", "voyageai/voyage-3"]),
    default="voyage/voyage-large-2-instruct",
)
@click.option(
    "--tokenization-alg",
    type=click.Choice(["voyageai/voyage"]),
    default="voyageai/voyage",
    help="tokenization algorithm",
)
@click.option(
    "--reduce-strategy",
    type=click.Choice([m.value for m in ReducingStrategy]),
    default="average",
    help="reducing strategy",
)
@click.option(
    "--max-tokens",
    type=int,
    default=16000,
    help="max tokens",
)
@click.option(
    "-n",
    "--max-concurrent-requests",
    type=int,
    default=100,
    help="max concurrent requests",
)
def async_create_syntatic_data_embeddings(
    src_db,
    model_name,
    prompt_type,
    embedding_model,
    tokenization_alg,
    reduce_strategy,
    max_tokens,
    max_concurrent_requests,
):
    assert os.getenv("VOYAGE_API_KEY") is not None, "VOYAGE_API_KEY is not set"
    reduce_strategy = ReducingStrategy(reduce_strategy)
    conn = get_db_connection(src_db, auto_commit=True)
    data = get_syntactic_data(
        conn,
        model_name,
        prompt_type,
        embedding_model,
        tokenization_alg,
        reduce_strategy,
    )
    text_data = [row[0] for row in data]
    s_ids = [row[1] for row in data]
    logger.debug(f"found {len(data)} embeddings to generate")
    if len(data) == 0:
        logger.info("No embeddings to generate")
        return
    asyncio.run(
        batch_get_embeddings(
            text_data,
            s_ids,
            embedding_model,
            max_tokens,
            tokenization_alg,
            reduce_strategy,
            src_db=src_db,
            max_concurrent=max_concurrent_requests,
        )
    )
    #         s_ids,
    #         model_name,
    #         max_tokens,
    #         tokenization_alg,
    #         reduce_strategy,
    #         None,
    #     )
    # )
    # )
    #         s_ids,
    #         model_name,
    #         max_tokens,
    #         tokenization_alg,
    #         reduce_strategy,
    #         None,
    #     )
    # )
    # )
    #         reduce_strategy,
    #         None,
    #     )
    # )
    # )


@dataops.command("update-extracted-content")
@click.option("-s", "--src-db", type=str, default="./db.sqlite3", help="source db")
def update_extracted_content(src_db):
    conn = get_db_connection(src_db, auto_commit=True)
    cur = conn.cursor()
    # get number of rows updated
    cur.execute(
        "UPDATE SyntaticData SET extracted_content = text WHERE extracted_content IS NULL"
    )
    conn.commit()
    num_rows_updated = cur.rowcount
    logger.info(f"Updated {num_rows_updated} rows")
    conn.close()


@dataops.command("bert-embedding")
@click.option("-s", "--src-db", type=str, default="./db.sqlite3", help="source db")
@click.option(
    "--model-name", type=str, default="distilbert-base-uncased", help="model name"
)
@click.option(
    "--status",
    type=click.Choice(["Accepted", "Rejected", "Language", "Music", "Kept"]),
    default="Accepted",
    help="status of the resource",
)
@click.option("--chunk-size", type=int, default=512, help="chunk size")
@click.option(
    "--reduce-strategy",
    type=click.Choice([m.value for m in ReducingStrategy]),
    default="average",
    help="reducing strategy",
)
def get_bert_embedding(src_db, model_name, status, chunk_size, reduce_strategy):
    conn = get_db_connection(src_db, auto_commit=True)
    query = """
    SELECT DISTINCT R.id, R.content FROM Resources R
    JOIN TopicResourceLink TRL on TRL.resource_id = R.id
    WHERE TRL.status = ? and R.content is not null
    """
    cur = conn.cursor()
    cur.execute(query, (status,))
    rows = cur.fetchall()
    pbar = tqdm(total=len(rows), colour="green")
    reduce_strategy = ReducingStrategy(reduce_strategy)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    encoding_name = model_name
    for row in rows:
        res_id = row[0]
        content = row[1]
        embedding = get_len_safe_bert_embedding(
            res_id,
            content,
            model,
            tokenizer,
            chunk_size,
            encoding_name,
            model_name,
            reduce_strategy,
            conn

        )
        pbar.update(1)
        pbar.set_description(f"{res_id=}, {len(embedding)=}")
    pbar.close()
    conn.close()
