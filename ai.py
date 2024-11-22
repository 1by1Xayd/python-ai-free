import requests
import json
from dataclasses import dataclass
from typing import List, Optional, Any
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

API_URL = "https://www.blackbox.ai/api/chat"
TO_CLEAN = ["Generated by BLACKBOX.AI, try unlimited chat https://www.blackbox.ai"]

@dataclass(frozen=True)
class Models:
    GPT4O: str = "gpt-4o"
    GEMINI_PRO: str = "gemini-pro"
    CLAUDE_SONNET: str = "claude-sonnet-3.5"
    BASIC: Any = None

@dataclass(frozen=True)
class AgentMode:
    id: str
    mode: bool
    name: str

@dataclass(frozen=True)
class Modes:
    IMAGE_GENERATION: AgentMode = AgentMode(
        id="ImageGenerationLV45LJp",
        mode=True,
        name="Image Generation"
    )

@dataclass
class Message:
    content: str
    role: str

class Chat:
    def __init__(
        self,
        model: Optional[str] = None,
        code_model_mode: bool = False,
        temperature: float = 0.7
    ):
        self.messages: List[Message] = []
        self.code_model_mode = code_model_mode
        self.clicked_answer2 = False
        self.clicked_answer3 = False
        self.clicked_force_web_search = False
        self.agent_mode = AgentMode(id="", mode=False, name="")
        self.trending_agent_mode = AgentMode(id="", mode=False, name="")
        self.max_tokens = 1024
        self.user_system_prompt = ""
        self.playground_temperature = temperature
        self.user_selected_model = model
        
        self._session = requests.Session()
        
        self._executor = ThreadPoolExecutor(max_workers=4)

    def __del__(self):
        self._session.close()
        self._executor.shutdown(wait=False)

    @lru_cache(maxsize=128)  # Cache responses for identical requests
    def _post_api(self, data: str) -> str:
        try:
            response = self._session.post(
                API_URL,
                data=data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            result = response.text
            
            for clean_text in TO_CLEAN:
                result = result.replace(clean_text, "")
            
            return result
        except Exception as e:
            raise RuntimeError(f"API request failed: {str(e)}")

    def send_message(self, message: Message) -> str:
        self.messages.append(message)
        
        payload = {
            "messages": [{"content": m.content, "role": m.role} for m in self.messages],
            "codeModelMode": self.code_model_mode,
            "clickedAnswer2": self.clicked_answer2,
            "clickedAnswer3": self.clicked_answer3,
            "clickedForceWebSearch": self.clicked_force_web_search,
            "agentMode": self.agent_mode.__dict__,
            "trendingAgentMode": self.trending_agent_mode.__dict__,
            "maxTokens": self.max_tokens,
            "userSystemPrompt": self.user_system_prompt,
            "playgroundTemperature": self.playground_temperature,
            "userSelectedModel": self.user_selected_model
        }
        
        json_data = json.dumps(payload)
        
        response = self._post_api(json_data)
        
        self.messages.append(Message(content=response, role="assistant"))
        
        return response

MODELS = Models()
MODES = Modes()
