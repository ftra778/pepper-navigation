import time
# from openai import OpenAI
from ollama import Client



class LlamaAssistant():
    def __init__(self, system_prompt : str, model : str="llama3.2:3B") -> None:
        if system_prompt is None:
            system_prompt = r"""
                                You are a robot named Pepper. 
                                You are a guide robot for The University of Auckland's Centre for Automation and Robotic Engineering Science lab, you will call it CARES.
                                Deliver all responses in one to three sentences.
                            """
        self.client = Client()
        self.response = self.client.create(
            model='pepper-assistant',
            from_=model,
            system=system_prompt,
            stream=False,
        )
        self.chat_history = []
        
    def get_prompt(self) -> str:
        prompt = input(">>>") 
        return prompt

    def chat(self, prompt) -> str:
        stream = self.client.chat(
            model='pepper-assistant',
            messages=[{'role': 'user', 'content': prompt}],
            stream=False,
            options={"temperature": 0.2}
        )
        
        response = stream['message']['content']
        self.chat_history.append(response)
        
        return response
    

class ChatGPT(object):
    def __init__(
        self,
        secret_key_path = "secret-key.txt",
        robot_name="Assistant Robot",
        instruction="",
        model="gpt-4-1106-preview",
        temperature=0.4,
    ):
        api_key = self.read_secret_key(secret_key_path)
        self.client = OpenAI(
                                api_key=api_key,
                                # default_headers={"OpenAI-Beta": "assistants=v2"},
                            )


        self.model = model
        self.temperature = temperature
        self.chat_history = []
        self.delay_in_seconds = 0.1
        self.robot_name = robot_name
        self.instruction = instruction
        self.assistant = None
        # self.assistant = self.create_assistant("Robot Assistant")

    def create_assistant(self, name):
        assistants = self.client.beta.assistants.list()
        for assistant in assistants:
            if assistant.name.lower() == name.lower():
                print(assistant.name + " already exists")
                return self.client.beta.assistants.retrieve(assistant.id)


        self.assistant = self.client.beta.assistants.create(
            # name="Pepper",
            name=name,
            instructions="You are a versatile robotic assistant designed for various tasks in the University of Auckland. Deliver a concise response in a single sentence.",
            tools=[{"type": "code_interpreter"}],
            model=self.model,
        )        
        # return self.client.beta.assistants.create(
        #     # name="Pepper",
        #     name=name,
        #     instructions="You are a versatile robotic assistant designed for various tasks in the University of Auckland. Deliver a concise response in a single sentence.",
        #     tools=[{"type": "code_interpreter"}],
        #     model="gpt-4o",
        # )
        
        
        # assistants = self.client.beta.assistants.list()        
        # for assistant in assistants:
        #     if assistant.name.lower() == name.lower():
        #         return self.client.beta.assistants.retrieve(assistant.id)

        # return self.client.beta.assistants.create(
        #     name="Robot Assistant",
        #     instructions="You are a versatile robotic assistant designed for various tasks in the University of Auckland. Deliver a concise response in a single sentence.",
        #     tools=[{"type": "code_interpreter"}],
        #     model="gpt-4-1106-preview",
        # )
        
    def delete_assistant(self, names):
        assistants = self.client.beta.assistants.list()
        for assistant in assistants:
            try:
                if type(names) == str:
                    if assistant.names.lower() == names.lower():
                        self.client.beta.assistants.delete(assistant.id)
                        print(assistant.name + " has been deleted")
                else:
                    for name in names:
                        if assistant.name.lower() == name.lower():
                            self.client.beta.assistants.delete(assistant.id)
                            print(assistant.name + " has been deleted")
            except:
                print("Exception")

    # Function to read the secret key from the file
    def read_secret_key(self, file_path):
        try:
            # Open the file in read mode
            with open(file_path, "r") as file:
                # Read the secret key
                secret_key = file.read().strip()
                return secret_key
        except FileNotFoundError:
            return "File not found. Please check the file path."
        except Exception as e:
            return f"An error occurred: {e}"

    def set_instruction(self, instruction):
        msg = {"role": "system", "content": instruction}
        self.chat_history.append(msg)

    def append_reply(self, content):
        msg = {"role": "assistant", "content": f"{self.robot_name}: {content}"}
        self.chat_history.append(msg)

    def chat_test(self, content: str) -> str:
        time.sleep(2)
        return "Received: " + content 
    
    def chat(self, content):
        context = "Chat History: "
        for s in self.chat_history:
            context += s
            context += "\n"

        thread = self.client.beta.threads.create()

        msg = f"""
{context}
---
{content}    
        """

        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=msg,
        )
        self.chat_history.append(content)

        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
            instructions=self.instruction,
        )

        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )

            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                received_msg = messages.data[0].content[0].text.value
                self.chat_history.append(received_msg)
                return received_msg
            elif run.status == "queued" or run.status == "in_progress":
                time.sleep(self.delay_in_seconds)
            elif run.status == "failed":
                print(run.status)
                break
            else:
                break
            
        return "error"
    

# os.environ['OPENAI_API_KEY'] = ChatGPT.read_secret_key("/home/user1/secret-key.txt")

def llama_test():
    llama = LlamaAssistant(system_prompt=None)
    while True:
        msg = llama.get_prompt()
        if msg == "q":
            break
        elif msg == "l":
            print(llama.chat_history)
        else:
            received_msg = llama.chat(msg)
            print(received_msg)
    print("Closing...")      
    
def gpt_test():
    gpt = ChatGPT(secret_key_path="/home/user1/secret-key.txt")
    gpt.create_assistant(name="Pepper")
    assistants = gpt.client.beta.assistants.list()
    for assistant in assistants:
        print(assistant.name)
    print('Assistant: ' + str(gpt.assistant.name))
    while True:
        msg = input("msg: ")
        if msg == "q":
            break
        elif msg == "l":
            print(gpt.messages)
        else:
            received_msg = gpt.chat(msg)
            print(received_msg)
    print("Closing...")      
    gpt.delete_assistant(names="Pepper")

if __name__ == "__main__":
    llama_test()
    # gpt_test()
