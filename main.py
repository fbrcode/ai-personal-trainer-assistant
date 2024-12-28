# code source: https://github.com/pdichone/vincibits-personal-trainer-assistant/tree/main

import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging

load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")

# defaults to getting the key using os.environ.get("OPENAI_API_KEY" )
# if you saved the key under a different environment variable name, use...
# client = OpenAI( api_key=os.environ.get ("CUSTOM_ENV_NAME" ) )

client = openai.OpenAI()
model = "gpt-4o-mini"

# === assistant creation
# personal_trainer_assistant = openai.beta.assistants.create(
#   name="Personal Trainer",
#   instructions="""You are the best personal trainer and nutritionist who knows how to get clients to build lean muscles.\n
#   You've trained high-caliber athletes and movie stars.""",
#   model=model,
# )
# assistant_id = personal_trainer_assistant.id

# === thread creation
# thread = client.beta.threads.create(
#   messages=[
#     {
#       "role": "user", 
#       "content": "How do I get started working out to lose fat and build muscles?"
#     },
#   ],
# )
# thread_id = thread.id

# === hardcoded assistant and thread ids
assistant_id = "asst_3qjhdpE56Y85ZKJBu8rpVyjf"
thread_id = "thread_DwLPCtlL1jsm4OMrPCuJpEEq"

# print(assistant_id)
# print(thread_id)

# === message creation
content1 = "What are the best exercises for lean muscles and getting strong?"
content2 = "How much water should I drink to get healthier?"
content3 = "How many reps do I need to do to build lean muscles?"
message = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=content3)

# === run assistant
run = client.beta.threads.runs.create(
  assistant_id=assistant_id,
  thread_id=thread_id,
  instructions="Please address the user as James Bond",
)
run_id = run.id

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Waits for a run to complete and prints the elapsed time.

    Args:
      client (openai.Client): The OpenAI client object.
      thread_id (str): The ID of the thread.
      run_id (str): The ID of the run.
      sleep_interval (int): Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# === run assistant
print("Running assistant...")
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run_id)

# ==== steps --- in order to get logs
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run_id)
print(f"Steps -> {run_steps.data[0]}")