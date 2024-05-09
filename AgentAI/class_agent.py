import google.generativeai as genai

class AgentAI:

    def __init__(self, gemini_key):
        self.gemini_key = gemini_key
        self.chat_agent = None
        self.agent = None
        genai.configure(api_key=self.gemini_key)

    def create_new_agent(self, agent_instruction, chat_agent=False):
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        self.chat_agent == chat_agent

        system_instruction = agent_instruction

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                    generation_config=generation_config,
                                    system_instruction=system_instruction)

        if self.chat_agent:
            self.agent = self.__create_chat_agent(model)
        else:
            self.agent = model
        return self.agent

    def __create_chat_agent(self, model):
        agent_model = model.start_chat(history=[])
        return agent_model

    def response(self, prompt):
        if self.chat_agent:
            convo.send_message(prompt)
            return convo.last.text
        else:
            response = self.agent.generate_content(prompt)
            return response.text