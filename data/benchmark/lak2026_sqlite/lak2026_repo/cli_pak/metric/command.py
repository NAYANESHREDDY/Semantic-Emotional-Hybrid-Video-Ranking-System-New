import click
import pandas as pd
from pathlib import Path
from loguru import logger
from metric_ops import (
    compute_baseline,
    agg_function,
    top_agg_function,
    compute_baseline_precision,
)
from db_ops import get_db_connection


QUERY = """
SELECT R.resource_order, E.which, TRL.status, E.value, C.title as course_title,T.title as topic_title, R.url 
FROM EmbeddingVectors as E
JOIN Resources as R on E.resource_id = R.id
JOIN TopicResourceLink as TRL on TRL.resource_id = R.id
JOIN Topics as T on TRL.topic_id = T.id
JOIN Courses as C on T.course_id = C.id
WHERE T.title NOT IN ("Time Management : Eisenhower Matrix")
"""
PRECISION_QUERY = """
SELECT R.resource_order, E.which, TRL.status, E.value, C.title as course_title, T.title as topic_title, R.url
FROM EmbeddingVectors as E
JOIN Resources as R on E.resource_id = R.id
JOIN TopicResourceLink as TRL on TRL.resource_id = R.id
JOIN Topics as T on TRL.topic_id = T.id
JOIN Courses as C on T.course_id = C.id
WHERE T.title NOT IN ("Time Management : Eisenhower Matrix")
  AND T.title IN (
      SELECT T2.title
      FROM Topics T2
      JOIN TopicResourceLink TRL2 ON TRL2.topic_id = T2.id
      WHERE TRL2.status = "Accepted"
      GROUP BY T2.title
      HAVING COUNT(*) > 1
  )
"""


def load_filtered_data(conn, topic=None, query=QUERY):
    df = pd.read_sql_query(query, conn)

    if topic:
        assert topic in df["topic_title"].unique(), (
            f"Topic {topic} not found in the database."
        )
        df = df[df["topic_title"] == topic]
    return df


def save_json(dataframe, dest_root, file_name):
    dest_file = Path(dest_root) / f"{file_name}.json"
    with open(dest_file, "w", encoding="utf-8") as f:
        dataframe.to_json(f, orient="records", lines=True)
    logger.info(f"Data saved to {dest_file}")


@click.group(name="metric")
def metric():
    """Commands for evaluating the performance of a model."""
    pass


@metric.command(name="acc-baseline")
@click.option(
    "-s",
    "--src-db",
    type=click.Path(exists=True),
    required=True,
    help="Path to the source database.",
)
@click.option(
    "-d",
    "--dest-root",
    type=click.Path(),
    required=True,
    help="Path to the destination directory.",
)
@click.option(
    "-t",
    "--topic",
    type=str,
    default=None,
    help="Topic name to filter; if None, all topics will be used.",
)
@click.option(
    "--file-name",
    type=str,
    default="baseline_acc",
    help="File name to save the baseline data (JSON format).",
)
def compute_baseline_cli(src_db, dest_root, topic, file_name):
    """Compute the baseline for the given topic data."""
    conn = get_db_connection(src_db)
    logger.info("Computing baseline score")
    df = load_filtered_data(conn, topic)

    one_per_topic = df.drop_duplicates(
        subset=["course_title", "topic_title", "status", "url"]
    )

    baseline = (
        one_per_topic.groupby(["course_title", "topic_title"], group_keys=False)
        .apply(compute_baseline)
        .apply(pd.Series)
        .reset_index()
    )
    baseline["baseline_performance"] = baseline["baseline_ok"] / (
        baseline["baseline_ok"] + baseline["baseline_nok"]
    )

    save_json(baseline, dest_root, file_name)


@metric.command(name="acc-embedding")
@click.option(
    "-s",
    "--src-db",
    type=click.Path(exists=True),
    required=True,
    help="Path to the source database.",
)
@click.option(
    "-d",
    "--dest-root",
    type=click.Path(),
    required=True,
    help="Path to the destination directory.",
)
@click.option(
    "-t",
    "--topic",
    type=str,
    default=None,
    help="Topic name to filter; if None, all topics will be used.",
)
@click.option(
    "--file-name",
    type=str,
    default="embedding_acc",
    help="File name to save the embedding performance data (JSON format).",
)
def compute_embedding_cli(src_db, dest_root, topic, file_name):
    """Compute the embedding performance for the given topic data."""
    conn = get_db_connection(src_db)
    logger.info("Computing embedding performance score")
    df = load_filtered_data(conn, topic)

    metric = (
        df.groupby(["which", "course_title", "topic_title"], group_keys=False)
        .apply(agg_function)
        .apply(pd.Series)
        .reset_index()
    )
    metric["embedding_performance"] = metric["ok"] / (metric["ok"] + metric["not_ok"])

    save_json(metric, dest_root, file_name)


@metric.command(name="precision-baseline")
@click.option(
    "-s",
    "--src-db",
    type=click.Path(exists=True),
    required=True,
    help="Path to the source database.",
)
@click.option(
    "-d",
    "--dest-root",
    type=click.Path(),
    required=True,
    help="Path to the destination directory.",
)
@click.option(
    "-t",
    "--topic",
    type=str,
    default=None,
    help="Topic name to filter; if None, all topics will be used.",
)
@click.option(
    "--file-name",
    type=str,
    default="precision_baseline",
    help="File name to save the precision data (JSON format).",
)
@click.option(
    "--at-n",
    type=int,
    default=5,
    help="Number of top items to consider for precision calculation.",
)
def compute_precision_cli(src_db, dest_root, topic, file_name, at_n):
    """Compute the precision for the given topic data."""
    conn = get_db_connection(src_db)
    logger.info("Computing precision score")
    df = load_filtered_data(conn, topic, PRECISION_QUERY)
    one_per_topic = df.drop_duplicates(
        subset=["course_title", "topic_title", "status", "url"]
    )
    metric = (
        one_per_topic.groupby(["course_title", "topic_title"], group_keys=False)
        .apply(compute_baseline_precision, at_n=at_n)
        .apply(pd.Series)
        .reset_index()
    )
    metric["baseline_precision"] = metric["baseline_precision"].astype(float)
    metric.rename(
        columns={
            "baseline_precision": f"baseline_precision_at_{at_n}",
        },
        inplace=True,
    )
    save_json(metric, dest_root, f"{file_name}_at_{at_n}")


@metric.command(name="precision-embedding")
@click.option(
    "-s",
    "--src-db",
    type=click.Path(exists=True),
    required=True,
    help="Path to the source database.",
)
@click.option(
    "-d",
    "--dest-root",
    type=click.Path(),
    required=True,
    help="Path to the destination directory.",
)
@click.option(
    "-t",
    "--topic",
    type=str,
    default=None,
    help="Topic name to filter; if None, all topics will be used.",
)
@click.option(
    "--file-name",
    type=str,
    default="precision_embedding",
    help="File name to save the precision data (JSON format).",
)
@click.option(
    "--at-n",
    type=int,
    default=5,
    help="Number of top items to consider for precision calculation.",
)
def compute_precision_embedding_cli(src_db, dest_root, topic, file_name, at_n):
    """Compute the precision for the given topic data."""
    conn = get_db_connection(src_db)
    logger.info("Computing precision score")
    df = load_filtered_data(conn, topic, PRECISION_QUERY)

    metric = (
        df.groupby(["which", "course_title", "topic_title"], group_keys=False)
        .apply(lambda df: top_agg_function(df, at_n=at_n))
        .apply(pd.Series)
        .reset_index()
    )
    metric["precision_at_n"] = metric["precision_at_n"].astype(float)
    metric.rename(
        columns={
            "precision_at_n": f"emb_precision_at_{at_n}",
        },
        inplace=True,
    )

    save_json(metric, dest_root, f"{file_name}_at_{at_n}")
