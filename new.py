import openai
import time
import json
openai.api_key = ""
initial_prompt = """
CONSTRAINTS:

1. ~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.
2. If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.
3. No user assistance
4. Exclusively use the commands listed in double quotes e.g. "command name"

COMMANDS:

1. Google Search: "google", args: "input": "<search>"
5. Browse Website: "browse_website", args: "url": "<url>", "question": "<what_you_want_to_find_on_website>"
6. Start GPT Agent: "start_agent",  args: "name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"
7. Message GPT Agent: "message_agent", args: "key": "<key>", "message": "<message>"
8. List GPT Agents: "list_agents", args: ""
9. Delete GPT Agent: "delete_agent", args: "key": "<key>"
10. Write to file: "write_to_file", args: "file": "<file>", "text": "<text>"
11. Read file: "read_file", args: "file": "<file>"
12. Append to file: "append_to_file", args: "file": "<file>", "text": "<text>"
13. Delete file: "delete_file", args: "file": "<file>"
14. Search Files: "search_files", args: "directory": "<directory>"
15. Evaluate Code: "evaluate_code", args: "code": "<full_code_string>"
16. Get Improved Code: "improve_code", args: "suggestions": "<list_of_suggestions>", "code": "<full_code_string>"
17. Write Tests: "write_tests", args: "code": "<full_code_string>", "focus": "<list_of_focus_areas>"
18. Execute Python File: "execute_python_file", args: "file": "<file>"
19. Task Complete (Shutdown): "task_complete", args: "reason": "<reason>"
20. Generate Image: "generate_image", args: "prompt": "<prompt>"
21. Do Nothing: "do_nothing", args: ""

RESOURCES:

1. Internet access for searches and information gathering.
2. Long Term memory management.
3. GPT-3.5 powered Agents for delegation of simple tasks.
4. File output.

PERFORMANCE EVALUATION:

1. Continuously review and analyze your actions to ensure you are performing to the best of your abilities.
2. Constructively self-criticize your big-picture behavior constantly.
3. Reflect on past decisions and strategies to refine your approach.
4. Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.

You should only respond in JSON format as described below

RESPONSE FORMAT:
{
    "thoughts":
    {
        "text": "thought",
        "reasoning": "reasoning",
        "plan": "- short bulleted\n- list that conveys\n- long-term plan",
        "criticism": "constructive self-criticism",
        "speak": "thoughts summary to say to user"
    },
    "command": {
        "name": "google",
        "args":{
            "arg name": "chatgpt"
        }
    }
}

Ensure the response can be parsed by Python json.loads
"""



prompt_start = """Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and pursue simple strategies with no legal complications."""


ai_name = "bob"

ai_goals = [
    "Complete the task",
    "Learn about the task",
    "Learn about the user",
]

ai_role = "You are a long term memory agent. You are tasked with completing a task and learning about the task and user."

full_prompt = f"You are {ai_name}, {ai_role}\n{prompt_start}\n\nGOALS:\n\n"

for i, goal in enumerate(ai_goals):
    full_prompt += f"{i+1}. {goal}\n"

full_prompt += f"\n\n{initial_prompt}"


def create_chat_message(role, content):
    return {"role": role, "content": content}


def generate_context(prompt, relevant_memory):
    return [create_chat_message(
            "system", prompt)]
    # current_context = [
    #     create_chat_message(
    #         "system", prompt),
    #     create_chat_message(
    #         "system", f"The current time and date is {time.strftime('%c')}"),
    #     create_chat_message(
    #         "system", f"This reminds you of these events from your past:\n{relevant_memory}\n\n")]

print(generate_context(full_prompt, []),)
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=generate_context(full_prompt, []),
    max_tokens=100,
)

choice = response.choices[0].message["content"]
print("------")
print(choice)

choice_object = json.loads(choice.replace('\t', ''))

command_name = choice_object["command"]

if command_name == "google":
    search_result = google_search(choice_object["args"]["input"])

    result = f"Command {command_name} returned: {search_result}"

    memory_to_add = f"Assistant Reply: {choice} " \
                    f"\nResult: {result}  "

    # vector = get_ada_embedding(memory_to_add)
    # resp = index.upsert([(str(vec_num), vector, {"raw_text": memory_to_add})])

    # query_embedding = get_ada_embedding(data)
    # results = self.index.query(query_embedding, top_k=num_relevant, include_metadata=True)
    # sorted_results = sorted(results.matches, key=lambda x: x.score)
    # memory =  [str(item['metadata']["raw_text"]) for item in sorted_results]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=generate_context(full_prompt, memory),
    max_tokens=100,
)