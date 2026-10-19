import asyncio
import re

from litellm import acompletion
from loguru import logger
from tenacity import (after_log, before_log, retry, stop_after_attempt,
                      wait_exponential)
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio

from db_ops import aget_db_connection


def extract_answer(text):
    match = re.search(
        r"<educational_content>(.*?)</educational_content>", text, re.DOTALL
    )
    if match:
        return match.group(1).strip()
    return None


async def get_synthetic_prompts(db_path, model_name, prompt_type):
    get_query = """
    SELECT P.id, P.topic_id, P.text 
    FROM Prompt P
    LEFT JOIN SyntaticData SD ON SD.prompt_id = P.id AND SD.model_name = ?
    WHERE SD.prompt_id IS NULL AND P.type = ?;
    """

    conn = await aget_db_connection(db_path)
    try:
        cursor = await conn.execute(get_query, (model_name, prompt_type))
        return await cursor.fetchall()
    finally:
        await conn.close()


async def save_synthetic_data_response(
    db_path,
    prompt_id,
    model_name,
    text,
    extracted_content,
    usage,
    temperature,
):
    """Insert response and usage data into SQLite database asynchronously"""
    try:
        insert_query = """INSERT INTO SyntaticData (prompt_id, text, extracted_content, model_name, temperature, prompt_tokens, completion_tokens, total_tokens) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)"""
        conn = await aget_db_connection(db_path)
        try:
            await conn.execute(
                insert_query,
                (
                    prompt_id,
                    text,
                    extracted_content,
                    model_name,
                    temperature,
                    usage["prompt_tokens"],
                    usage["completion_tokens"],
                    usage["total_tokens"],
                ),
            )
            await conn.commit()
        finally:
            await conn.close()
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")
        raise


def handle_failure(retry_state):
    # change the function to log the error observed in ret
    logger.error(f"Function failed after {retry_state.attempt_number} attempts")
    return None, None  # Return a default value or perform some other action


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=30, max=60),
    before=before_log(logger, "DEBUG"),
    after=after_log(logger, "INFO"),
    retry_error_callback=handle_failure,
)
async def get_response(user_message, model_name, temperature, system_prompt):
    response = await acompletion(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=temperature,
    )
    usage = response["usage"]
    content = response["choices"][0]["message"]["content"]
    if content is None:
        raise Exception("No content returned")
    return content, usage


async def process_synthetic_prompt(
    db_path, prompt_id, prompt_text, model_name, temperature, system_prompt
):
    response, usage = await get_response(
        prompt_text, model_name, temperature, system_prompt
    )
    extracted_content = extract_answer(response)
    await save_synthetic_data_response(
        db_path,
        prompt_id,
        model_name,
        response,
        extracted_content,
        usage,
        temperature,
    )


async def process_synthetic_prompts(
    db_path, model_name, prompt_type, temperature, system_prompt, max_concurrent_requests
):
    prompts = await get_synthetic_prompts(db_path, model_name, prompt_type)
    logger.debug(f"Processing {len(prompts)} prompts for {model_name}")
    tasks = []
    
    # Create overall progress bar
    total_pbar = tqdm(total=len(prompts), desc="Total progress", colour="green")
    
    for prompt_id, _, prompt_text in prompts:
        task = asyncio.create_task(
            process_synthetic_prompt(
                db_path,
                prompt_id,
                prompt_text,
                model_name,
                temperature,
                system_prompt,
            )
        )
        tasks.append(task)
        if len(tasks) >= max_concurrent_requests:
            await tqdm_asyncio.gather(
                *tasks, desc="Generating responses", colour="yellow"
            )
            # Update the total progress bar
            total_pbar.update(len(tasks))
            # sleep for 30 seconds
            await asyncio.sleep(5)
            tasks = []
    
    if tasks:
        await tqdm_asyncio.gather(*tasks, desc="Generating responses", colour="yellow")
        # Update the total progress bar for remaining tasks
        total_pbar.update(len(tasks))
    
    total_pbar.close()
