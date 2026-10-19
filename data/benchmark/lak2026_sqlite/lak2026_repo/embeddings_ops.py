import json
from itertools import islice

import numpy as np
from litellm import aembedding, embedding
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_random_exponential
from tokenizers import Tokenizer
from tqdm.asyncio import tqdm_asyncio

from db_ops import (
    ReducingStrategy,
    aget_db_connection,
    ainsert_syntactic_data_embedding,
    insert_embeddings_vector,
)
from transformers import AutoModel, AutoTokenizer
import torch


@retry(
    wait=wait_random_exponential(min=1, max=20),
    stop=stop_after_attempt(10),
)
def get_embedding(text, model_name, input_type, **kwargs):
    response = embedding(
        model=model_name,
        input=[text],
    )
    return response["data"][0]["embedding"], response["usage"]["total_tokens"]


@retry(
    wait=wait_random_exponential(min=1, max=20),
    stop=stop_after_attempt(10),
)
async def aget_embedding(text, model_name, input_type, **kwargs):
    """Async version of get_embedding function"""
    response = await aembedding(
        model=model_name,
        input=[text],
    )
    logger.info(f"got embedding for {text[:10]}")
    return response["data"][0]["embedding"], response["usage"]["total_tokens"]


def get_distilbert_embeddings(text, model, tokenizer):
    # Tokenize input text (truncate/pad to max 512 tokens)
    
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, padding=True, max_length=512
    )

    # Get model outputs (no gradients for inference)
    with torch.no_grad():
        outputs = model(**inputs)

    # Extract embeddings (last hidden state)
    embeddings = outputs.last_hidden_state

    # Pool embeddings (mean pooling across tokens)
    pooled_embeddings = torch.mean(embeddings, dim=1).squeeze().numpy()

    return pooled_embeddings


def reduce_weight_average(chunk_embeddings, chunk_lens):
    chunk_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
    chunk_embeddings = chunk_embeddings / np.linalg.norm(
        chunk_embeddings
    )  # normalizes length to 1
    chunk_embeddings = chunk_embeddings.tolist()
    return chunk_embeddings


def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def voyageai_chunked_text(text, encoding_name, chunk_length):
    tokenizer = Tokenizer.from_pretrained(encoding_name)
    tokenizer.no_truncation()
    # added new
    tokenizer.no_padding()
    encoding = tokenizer.encode(text)
    chunks_iterator = batched(encoding.ids, chunk_length)
    for chunk in chunks_iterator:
        yield tokenizer.decode(chunk)


def huggingface_chunked_text(text, encoding_name, chunk_length):
    tokenizer = AutoTokenizer.from_pretrained(encoding_name)
    encoding = tokenizer(text, return_tensors="pt")
    chunks_iterator = batched(encoding.input_ids.flatten(), chunk_length)
    for chunk in chunks_iterator:
        yield tokenizer.decode(chunk)


def chunked_tokens(text: str, encoding_name: str, chunk_length: int):
    match encoding_name:
        case "voyageai/voyage" | "voyageai/voyage-3":
            yield from voyageai_chunked_text(text, encoding_name, chunk_length)
        case "distilbert-base-uncased":
            yield from huggingface_chunked_text(text, encoding_name, chunk_length)
        case _:
            raise ValueError(f"Unsupported encoding name: {encoding_name}")

def len_safe_get_embedding(
    text,
    model_name,
    max_tokens,
    encoding_name,
    reducing_strategy=ReducingStrategy.AVERAGE,
    input_type=None,
):
    if reducing_strategy == ReducingStrategy.TRUNCATE:
        raise NotImplementedError("Truncate strategy is not implemented")
        # text = truncate_text_tokens(text, encoding_name, max_tokens)
        # return embedding_function(
        #     client, text, model_name=model_name, input_type=input_type
        # )
    else:
        chunk_embeddings = []
        chunk_lens = []
        usage = 0
        for chunk in chunked_tokens(
            text, encoding_name=encoding_name, chunk_length=max_tokens
        ):
            chunk_embedding, chunk_usage = get_embedding(
                chunk, model_name=model_name, input_type=input_type
            )
            chunk_embeddings.append(chunk_embedding)
            chunk_lens.append(len(chunk))
            usage += chunk_usage

        if reducing_strategy == ReducingStrategy.AVERAGE:
            return reduce_weight_average(chunk_embeddings, chunk_lens), usage
        elif reducing_strategy == ReducingStrategy.CONCAT:
            return np.concatenate(chunk_embeddings).tolist(), usage

        elif reducing_strategy == ReducingStrategy.CONCAT:
            return np.concatenate(chunk_embeddings).tolist(), usage


def get_len_safe_bert_embedding(
    resource_id,
    text,
    model,
    tokenizer,
    max_tokens,
    encoding_name,
    model_name,
    reducing_strategy=ReducingStrategy.AVERAGE,
    src_db=None,
):
    if reducing_strategy == ReducingStrategy.TRUNCATE:
        raise NotImplementedError("Truncate strategy is not implemented")

    chunk_embeddings = []
    chunk_lens = []
    for i, chunk in enumerate(
        chunked_tokens(text, encoding_name=encoding_name, chunk_length=max_tokens)
    ):
        chunk_embedding = get_distilbert_embeddings(chunk, model, tokenizer)
        chunk_embeddings.append(chunk_embedding)
        chunk_lens.append(len(chunk))
    if reducing_strategy == ReducingStrategy.AVERAGE:
        embedding = reduce_weight_average(chunk_embeddings, chunk_lens)
    elif reducing_strategy == ReducingStrategy.CONCAT:
        embedding = np.concatenate(chunk_embeddings).tolist()
    if src_db:
        try:    
            insert_embeddings_vector(
                src_db, resource_id, model_name, encoding_name, reducing_strategy, embedding, 0
            )
        except Exception as e:
            logger.error(f"Error inserting embedding: {e}")
            logger.error(f"{chunk_lens=}")
            logger.error(f"{resource_id=}")
    return embedding


async def alen_safe_get_embedding(
    text,
    syntactic_data_id,
    model_name,
    max_tokens,
    encoding_name,
    reducing_strategy=ReducingStrategy.AVERAGE,
    input_type=None,
    src_db=None,
    max_concurrent=5,
):
    if reducing_strategy == ReducingStrategy.TRUNCATE:
        raise NotImplementedError("Truncate strategy is not implemented")

    chunk_embeddings = []
    chunk_lens = []
    usage = 0

    async def process_chunk(chunk):
        # logger.info(f"getting embedding for {chunk[:10]}")
        chunk_embedding, chunk_usage = await aget_embedding(
            chunk, model_name=model_name, input_type=input_type
        )
        return chunk_embedding, chunk_usage, len(chunk)

    # Create tasks for all chunks
    tasks = [
        process_chunk(chunk)
        for chunk in chunked_tokens(
            text, encoding_name=encoding_name, chunk_length=max_tokens
        )
    ]

    # Execute all chunks in parallel
    # results = await asyncio.gather(*tasks)
    if len(tasks) > 1:
        results = await tqdm_asyncio.gather(
            *tasks, desc="Getting embeddings", colour="green"
        )
    else:
        results = [await tasks[0]]
    # Process results
    for chunk_embedding, chunk_usage, chunk_len in results:
        chunk_embeddings.append(chunk_embedding)
        chunk_lens.append(chunk_len)
        usage += chunk_usage

    if reducing_strategy == ReducingStrategy.AVERAGE:
        embedding = reduce_weight_average(chunk_embeddings, chunk_lens)
    elif reducing_strategy == ReducingStrategy.CONCAT:
        embedding = np.concatenate(chunk_embeddings).tolist()

    if src_db:
        await ainsert_syntactic_data_embedding(
            src_db,
            syntactic_data_id,
            model_name,
            encoding_name,
            reducing_strategy.value,
            json.dumps(embedding),
            usage,
        )
    return embedding, usage


async def batch_get_embeddings(
    texts: list[str],
    syntactic_data_id: list[int],
    model_name: str,
    max_tokens: int,
    encoding_name: str,
    reducing_strategy=ReducingStrategy.AVERAGE,
    src_db: str = None,
    input_type=None,
    max_concurrent=5,
):
    """Process multiple texts in parallel to get their embeddings."""
    tasks = [
        alen_safe_get_embedding(
            text,
            syntactic_data_id,
            model_name=model_name,
            max_tokens=max_tokens,
            encoding_name=encoding_name,
            reducing_strategy=reducing_strategy,
            input_type=input_type,
            src_db=src_db,
            max_concurrent=max_concurrent,
        )
        for text, syntactic_data_id in zip(texts, syntactic_data_id)
    ]
    return await tqdm_asyncio.gather(*tasks, desc="Getting embeddings", colour="green")
