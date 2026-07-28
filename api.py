import sys
import os
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Ensure the src folder is in path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from app import get_llm_provider, parse_action, execute_tool
from prompts import REACT_SYSTEM_PROMPT, MAX_ITERATIONS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import List, Dict

class ChatRequest(BaseModel):
    query: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    answer: str
    thoughts: list[str]

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    provider = get_llm_provider()
    user_query = request.query
    
    conversation_history = ""
    for msg in request.history:
        role = "User Question" if msg.get("role") == "user" else "Final Answer"
        conversation_history += f"{role}: {msg.get('content')}\n"
        
    conversation_history += f"User Question: {user_query}\n"
    step = 0
    thoughts_list = []
    
    while step < MAX_ITERATIONS:
        step += 1
        
        prompt = conversation_history + "\nThought:"
        llm_response = provider.generate(prompt, system_prompt=REACT_SYSTEM_PROMPT)
        
        if not llm_response.startswith("Thought:"):
            llm_response = "Thought: " + llm_response.strip()
            
        if "Action:" in llm_response:
            thought_part = llm_response.split("Action:")[0].strip()
            action_part = "Action:" + llm_response.split("Action:")[1].strip()
            if thought_part:
                thoughts_list.append(thought_part)
            thoughts_list.append(action_part)
        else:
            thoughts_list.append(llm_response)
            
        conversation_history += f"\n{llm_response}"
        
        if "Final Answer:" in llm_response:
            final_answer = llm_response.split("Final Answer:")[-1].strip()
            return ChatResponse(answer=final_answer, thoughts=thoughts_list)
            
        action_match = re.search(r"Action:\s*(.+)", llm_response)
        if action_match:
            action_str = action_match.group(1).strip()
            tool_name, args = parse_action(action_str)
            
            observation = execute_tool(tool_name, args)
            obs_text = f"Observation: {observation}"
            thoughts_list.append(obs_text)
            
            conversation_history += f"\n{obs_text}"
        else:
            obs_text = "Observation: Hãy tiếp tục suy luận (Thought) hoặc đưa ra Action/Final Answer."
            thoughts_list.append(obs_text)
            conversation_history += f"\n{obs_text}"
            
    return ChatResponse(answer="LỖI: Đã đạt giới hạn tối đa bước suy luận.", thoughts=thoughts_list)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
