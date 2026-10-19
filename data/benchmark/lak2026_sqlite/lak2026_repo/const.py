# prepare a const variable which is a list and called provides that contain few strings
# and then use it in the code

providers = []
openai_models_list = [
    "gpt-4o",
    "o1-mini",
    "o3-mini",
    "gpt-4o-mini",
    "gpt-3.5-turbo-0125",
]
providers.extend([f"openai/{model}" for model in openai_models_list])

google_models_list = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]
providers.extend([f"gemini/{model}" for model in google_models_list])

providers.extend(["anthropic/claude-3-5-sonnet-20240620"])


# PROMPTS

PROMPT_WITH_COGNITIVE_IMPAIRMENT = """You will be generating educational content based on a given topic title. The content should be in English and should effectively teach and explain the topic to the readers with cognitive impairments.

Here is the topic title:
<topic_title>
{TOPIC_TITLE}
</topic_title>

To guide your content generation, here is an example of relevant content on the topic:
<example_content>
{EXAMPLE_CONTENT}
</example_content>

Using the topic title and the example content as a reference, generate new educational content that thoroughly explains the topic. The content should be original and not copied from the example. Ensure that the content is accessible and suitable for learners with cognitive impairments.

<scratchpad>
- Identify the key points and concepts from the topic title and example content
- Outline a structure for the educational content, ensuring a logical flow of information
- Expand on each point, providing clear explanations, examples, and analogies as needed
- Ensure the content is engaging, informative, and suitable for the target audience
</scratchpad>

Please provide your generated educational content inside <educational_content> tags."""

PROMPT_WITHOUT_COGNITIVE_IMPAIRMENT = """
You will be generating educational content based on a given topic title. The content should be in English and should effectively teach and explain the topic.

Here is the topic title:
<topic_title>
{TOPIC_TITLE}
</topic_title>

To guide your content generation, here is an example of relevant content on the topic:
<example_content>
{EXAMPLE_CONTENT}
</example_content>

Using the topic title and the example content as a reference, generate new educational content that thoroughly explains the topic. The content should be original and not copied from the example. 

<scratchpad>
- Identify the key points and concepts from the topic title and example content
- Outline a structure for the educational content, ensuring a logical flow of information
- Expand on each point, providing clear explanations, examples, and analogies as needed
- Ensure the content is engaging, informative, and suitable for the target audience
</scratchpad>

Please provide your generated educational content inside <educational_content> tags."""


PROMPT_COG_LR_BASES_INSTRUCTION = """
Give me simple and easy-to-understand educational content about {TOPIC_TITLE}. The content should be step-by-step, using clear language, short sentences, and practical examples. It should cover these topics:
{LEARNING_OUTCOMES}
"""

PROMPT_LR_BASE_BRIEF = """Give me simple and easy-to-understand educational content about {TOPIC_TITLE}. The content must be brief and cover these topics: {LEARNING_OUTCOMES}"""
