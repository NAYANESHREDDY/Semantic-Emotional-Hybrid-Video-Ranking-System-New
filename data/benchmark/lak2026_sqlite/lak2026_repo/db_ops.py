import json
import sqlite3
from enum import Enum
from sqlite3 import Error

import aiosqlite
from loguru import logger


class ReducingStrategy(Enum):
    AVERAGE = "average"
    CONCAT = "concat"
    TRUNCATE = "truncate"


def get_db_connection(db_file, auto_commit=True):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        if auto_commit:
            conn.isolation_level = None  # This is how SQLite handles autocommit
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("PRAGMA journal_mode = WAL")
        conn.commit()
        return conn
    except Error as e:
        logger.exception(e)
        raise e


def insert_embeddings_vector(
    conn,
    resource_id,
    embedding_model,
    tokenization_alg,
    reduction_alg,
    embedding,
    token_cost,
):
    query = """
    INSERT INTO EmbeddingVectors (which, tokenization_alg, reduction_alg, value, token_cost, resource_id) VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(
        query,
        (
            embedding_model,
            tokenization_alg,
            reduction_alg.value,
            json.dumps(embedding),
            token_cost,
            resource_id,
        ),
    )
    conn.commit()


async def aget_db_connection(db_path, autocommit=True):
    conn = await aiosqlite.connect(db_path, isolation_level=None, autocommit=autocommit)
    await conn.execute("PRAGMA foreign_keys = ON")
    await conn.execute("PRAGMA journal_mode = WAL")
    return conn


#


def get_syntactic_data(
    conn,
    model_name="openai/gpt-4o",
    prompt_type="without_cognitive_impairment",
    embedding_model="voyage-large-2-instruct",
    tokenization_alg="voyageai/voyage",
    reduction_alg=ReducingStrategy.AVERAGE,
    ignore_existing_embeddings=False,
):
    if ignore_existing_embeddings:
        query = """
        SELECT sd.extracted_content, sd.id as sd_id
        FROM SyntaticData sd
        JOIN Prompt p ON sd.prompt_id = p.id
        LEFT JOIN SyntacticDataEmbeddingVector sdev 
            ON sd.id = sdev.syntactic_data_id 
            AND sdev.which = ?
            AND sdev.tokenization_alg = ?
            AND sdev.reduction_alg = ?
        WHERE (? is NULL OR sd.model_name = ?)
            AND p.type = ?
            AND sd.extracted_content IS NOT NULL
        """
    else:
        query = """
        SELECT sd.extracted_content, sd.id as sd_id
        FROM SyntaticData sd
        JOIN Prompt p ON sd.prompt_id = p.id
        LEFT JOIN SyntacticDataEmbeddingVector sdev 
            ON sd.id = sdev.syntactic_data_id 
            AND sdev.which = ?
            AND sdev.tokenization_alg = ?
            AND sdev.reduction_alg = ?
        WHERE (? is NULL OR sd.model_name = ?)
            AND p.type = ?
            AND sdev.id IS NULL
            AND sd.extracted_content IS NOT NULL
        """

    cursor = conn.cursor()
    cursor.execute(
        query,
        (
            embedding_model,
            tokenization_alg,
            reduction_alg.value,
            model_name,
            model_name,
            prompt_type,
        ),
    )
    return cursor.fetchall()


def insert_syntactic_data_embedding(
    conn,
    syntactic_data_id,
    embedding_model,
    tokenization_alg,
    reduction_alg,
    embedding,
    token_cost,
):
    query = """
    INSERT INTO SyntacticDataEmbeddingVector (syntactic_data_id, which, tokenization_alg, reduction_alg, value, token_cost) VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(
        query,
        (
            syntactic_data_id,
            embedding_model,
            tokenization_alg,
            reduction_alg.value,
            embedding,
            token_cost,
        ),
    )
    conn.commit()


async def ainsert_syntactic_data_embedding(
    src_db,
    syntactic_data_id,
    embedding_model,
    tokenization_alg,
    reduction_alg,
    embedding,
    token_cost,
):
    try:
        query = """
        INSERT INTO SyntacticDataEmbeddingVector (syntactic_data_id, which, tokenization_alg, reduction_alg, value, token_cost) VALUES (?, ?, ?, ?, ?, ?)
        """
        conn = await aget_db_connection(src_db)
        await conn.execute(
            query,
            (
                syntactic_data_id,
                embedding_model,
                tokenization_alg,
                reduction_alg,
                embedding,
                token_cost,
            ),
        )
        await conn.commit()
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")
        raise
    finally:
        await conn.close()


def get_all_resources_given_topic_id(conn, topic_id, exclude_res_id):
    query = """
    SELECT r.id as res_id,r.url as res_url, ev.status as label, ev.value as embedding
    FROM Resource r
    JOIN TopicResourceLink t ON r.id = t.resource_id
    JOIN EmbeddingVector ev ON r.id = ev.resource_id
    WHERE t.topic_id = ?
    AND r.id != ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (topic_id, exclude_res_id))
    return cursor.fetchall()


def get_resource_id_given_url(url, conn):
    query = """
    SELECT id FROM Resources WHERE url = ?
    """
    cursor = conn.cursor()
    cursor.execute(query, (url,))
    return cursor.fetchone()[0]


def get_topic_given_res_id(res_id, conn):
    query = """
    SELECT topic_id from TopicResourceLink
    Where resource_id = ?
"""
    cursor = conn.cursor()
    cursor.execute(query, (res_id,))
    return cursor.fetchone()[0]
