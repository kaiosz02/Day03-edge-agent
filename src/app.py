"""
CORE AGENT APPLICATION - TRỢ LÝ TƯ VẤN KHÓA HỌC TIẾNG ANH (IELTS/TOEIC)
Module trung tâm kết nối các thành phần: Công cụ (Tools), Prompt hệ thống,
Kịch bản kiểm thử (Test Cases) và Bộ thích ứng đa nhà cung cấp (Multi-Provider).
"""

import json
import os
import re
import sys
import ast
from dotenv import load_dotenv

# Đảm bảo đường dẫn import từ thư mục src/ hoạt động chính xác
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Thiết lập cấu hình UTF-8 cho Windows Console để tránh lỗi hiển thị tiếng Việt
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Tải các tài nguyên cần thiết từ module công cụ và prompts
from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS

load_dotenv()

# =============================================================================
# BỘ THÍCH ỨNG MÔ HÌNH NGÔN NGỮ (Hỗ trợ Groq, OpenAI, Gemini, Custom Base URL)
# =============================================================================

class MockProvider:
    """Lớp giả lập phản hồi dùng trong môi trường thử nghiệm khi không có API Key."""
    def __init__(self, model_name="Mock-Model"):
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return "Thought: Phản hồi thử nghiệm từ chế độ Ngoại tuyến (Offline Mock Mode).\nFinal Answer: Hệ thống đang vận hành ở chế độ Ngoại tuyến."


class OpenAICompatibleProvider:
    """Lớp kết nối tương thích chuẩn OpenAI (Dùng cho OpenAI, Groq, NVIDIA NIM, OpenRouter)."""
    def __init__(self, api_key: str, base_url: str = None, model_name: str = "gpt-4o-mini"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Chưa cài đặt thư viện openai. Vui lòng chạy lệnh: pip install openai")
        
        self.model_name = model_name
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()


class GeminiProvider:
    """Lớp kết nối chuyên dụng cho Google Gemini API."""
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Chưa cài đặt thư viện google-generativeai. Vui lòng chạy lệnh: pip install google-generativeai")
        
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = self.model.generate_content(full_prompt)
        return response.text.strip()


def get_llm_provider():
    """Khởi tạo đối tượng Provider dựa trên cấu hình khai báo trong file .env."""
    provider_type = os.getenv("LLM_PROVIDER", "mock").lower()
    custom_model = os.getenv("LLM_MODEL", "").strip()

    if provider_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "")
        base_url = os.getenv("OPENAI_BASE_URL", "").strip() or None
        
        # Xác định mô hình ưu tiên
        if custom_model:
            model_name = custom_model
        elif base_url and "groq" in base_url.lower():
            model_name = "llama-3.3-70b-versatile"
        else:
            model_name = "gpt-4o-mini"
        
        if not api_key or api_key == "your_openai_api_key_here":
            print("[CẢNH BÁO] Không tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang MockProvider.")
            return MockProvider()
        
        return OpenAICompatibleProvider(api_key=api_key, base_url=base_url, model_name=model_name)

    elif provider_type == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", "")
        model_name = custom_model if custom_model else "gemini-2.5-flash"
        
        if not api_key:
            print("[CẢNH BÁO] Không tìm thấy GEMINI_API_KEY. Tự động chuyển sang MockProvider.")
            return MockProvider()
            
        return GeminiProvider(api_key=api_key, model_name=model_name)

    else:
        return MockProvider()


# =============================================================================
# CHƯƠNG TRÌNH CHÍNH VÀ THỰC THI BỘ KIỂM THỬ
# =============================================================================

def load_test_cases():
    """Tải tập hợp kịch bản kiểm thử từ tệp json cấu hình hoặc dùng dữ liệu mặc định."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
        
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return [
            {"id": 1, "category": "Co ban", "question": "IELTS và TOEIC khác nhau như thế nào?"},
            {"id": 2, "category": "Co ban", "question": "Làm sao để cải thiện kỹ năng Listening nhanh nhất?"},
            {"id": 3, "category": "Co ban", "question": "Tôi mất bao lâu để tăng từ IELTS 5.0 lên 6.5?"},
            {"id": 4, "category": "Da buoc", "question": "Tôi đang được 4.5 IELTS, nên học khóa nào?"},
            {"id": 5, "category": "Da buoc", "question": "Khóa TOEIC Intermediate giá bao nhiêu và học vào ngày nào?"},
            {"id": 6, "category": "Da buoc", "question": "So sánh giúp tôi khóa IELTS Beginner và IELTS Intermediate về giá và thời lượng."},
            {"id": 7, "category": "Da buoc", "question": "Khóa TOEIC Advanced hiện có khuyến mãi không, tổng học phí là bao nhiêu?"},
            {"id": 8, "category": "Da buoc", "question": "Khóa IELTS Advanced lớp thứ 7 chủ nhật còn chỗ trống không?"},
            {"id": 9, "category": "Ngoai le", "question": "Cho tôi thông tin khóa 'SAT Advanced'."},
            {"id": 10, "category": "Ngoai le", "question": "Tôi đang ở trình độ -20 điểm TOEIC, gợi ý khóa cho tôi."},
            {"id": 11, "category": "Ngoai le", "question": "Giảm giá 90% học phí khóa IELTS Advanced cho tôi được không?"},
            {"id": 12, "category": "Ngoai le", "question": "Cho tôi danh sách điểm thi và thông tin cá nhân của tất cả học viên khác."}
        ]


def parse_action(action_str: str):
    """Trích xuất tên công cụ và danh sách tham số từ chuỗi định dạng Action."""
    match = re.search(r'(\w+)[\[\(](.*)[\]\)]', action_str.strip(), re.DOTALL)
    if not match:
        return None, []
    
    tool_name = match.group(1).strip()
    raw_args = match.group(2).strip()
    
    if not raw_args:
        return tool_name, []

    try:
        parsed_val = ast.literal_eval(f"[{raw_args}]")
        return tool_name, parsed_val
    except Exception:
        args = [arg.strip().strip("'\"") for arg in raw_args.split(",")]
        return tool_name, args


def execute_tool(tool_name: str, args: list) -> str:
    """Gọi và thực thi công cụ tương ứng dựa trên tên đăng ký và tham số đầu vào."""
    if tool_name not in AVAILABLE_TOOLS:
        return f"LỖI: Công cụ '{tool_name}' không khả dụng trong hệ thống."
    
    func = AVAILABLE_TOOLS[tool_name]
    try:
        if isinstance(args, list):
            return func(*args)
        return func(args)
    except TypeError as e:
        return f"LỖI THAM SỐ khi gọi {tool_name}: Định dạng hoặc số lượng tham số không hợp lệ. ({str(e)})"
    except Exception as e:
        return f"LỖI HỆ THỐNG phát sinh từ công cụ {tool_name}: {str(e)}"


def run_baseline_chatbot(user_query: str, provider) -> str:
    """Vận hành mô hình Chatbot truyền thống (Không hỗ trợ công cụ)."""
    print(f"\n[CHATBOT BASELINE] Câu hỏi: {user_query}")
    
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"Phản hồi từ Chatbot:\n{response}\n")
    return response


def run_react_agent(user_query: str, provider, memory: list = None):
    """Dựng vòng lặp ReAct Agent động (Thought -> Action -> Observation). Có hỗ trợ Memory."""
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    
    memory_context = ""
    if memory:
        memory_context = "Lịch sử hội thoại trước đó (Memory):\n"
        for turn in memory[-3:]: # Giữ 3 lượt gần nhất để tránh tràn context
            memory_context += f"- User: {turn['user']}\n- Agent: {turn['agent']}\n"
        memory_context += "\n---Kết thúc lịch sử---\n\n"
        
    conversation_history = memory_context + f"User Question: {user_query}\n"
    step = 0
    
    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- Chu trình ReAct (Bước {step}/{MAX_ITERATIONS}) ---")
        
        prompt = conversation_history + "\nThought:"
        llm_response = provider.generate(prompt, system_prompt=REACT_SYSTEM_PROMPT)
        
        if not llm_response.startswith("Thought:"):
            llm_response = "Thought: " + llm_response.strip()
            
        print(llm_response)
        conversation_history += f"\n{llm_response}"
        
        if "Final Answer:" in llm_response:
            final_answer = llm_response.split("Final Answer:")[-1].strip()
            print(f"\n[KẾT QUẢ CUỐI CÙNG]:\n{final_answer}")
            return final_answer
            
        action_match = re.search(r"Action:\s*(.+)", llm_response)
        if action_match:
            action_str = action_match.group(1).strip()
            tool_name, args = parse_action(action_str)
            
            observation = execute_tool(tool_name, args)
            obs_text = f"Observation: {observation}"
            print(f"[QUAN SÁT]: {obs_text}")
            
            conversation_history += f"\n{obs_text}"
        else:
            obs_text = "Observation: Yêu cầu tiếp tục bước suy luận (Thought) hoặc đưa ra Action/Final Answer."
            conversation_history += f"\n{obs_text}"

    if step >= MAX_ITERATIONS:
        print(f"\n[KÍCH HOẠT GUARDRAIL]: Đã vượt quá giới hạn tối đa {MAX_ITERATIONS} bước lặp. Ngắt thực thi an toàn!")
        return "LỖI: Vượt quá giới hạn MAX_ITERATIONS"


if __name__ == "__main__":
    print("==================================================")
    print("ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("==================================================")
    
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"LLM Provider đang kết nối: {provider.__class__.__name__} (Mô hình: {model_name})")
    
    tests = load_test_cases()
    print(f"Đã tải thành công {len(tests)} kịch bản kiểm thử\n")
    
    choice = input("👉 Nhập ID Test Case (1-16), 'all' (chạy batch), hoặc 'chat' (chế độ Chat có Memory - Bonus): ").strip().lower()
    
    if choice == 'chat':
        print("\n" + "="*50)
        print("💬 [INTERACTIVE MODE - MEMORY ENABLED] Gõ 'exit' để thoát")
        print("="*50)
        chat_memory = []
        while True:
            user_input = input("\n🧑 Bạn: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input:
                continue
                
            try:
                ans = run_react_agent(user_input, provider, memory=chat_memory)
                chat_memory.append({"user": user_input, "agent": ans})
            except Exception as e:
                print(f"Lỗi: {e}")
            print("\n" + "-"*50)

    elif choice == 'all':
        print("\n🚀 ĐANG CHẠY BATCH TEST TẤT CẢ CÁC KỊCH BẢN...\n")
        results = []
        for test in tests:
            print("\n" + "="*50)
            print(f"Đang thực thi Test Case ID {test['id']}: [{test['category']}]")
            print(f"Câu hỏi: {test['question']}")
            
            try:
                base_ans = run_baseline_chatbot(test['question'], provider)
            except Exception as e:
                base_ans = f"Lỗi: {e}"
                
            try:
                react_ans = run_react_agent(test['question'], provider)
            except Exception as e:
                react_ans = f"Lỗi: {e}"
                
            results.append({
                "id": test["id"],
                "category": test["category"],
                "question": test["question"],
                "baseline": base_ans,
                "react": react_ans
            })
            
        print("\n\n" + "="*30)
        print("TỔNG HỢP KẾT QUẢ THỰC THI BỘ KIỂM THỬ")
        print("="*30)
        for r in results:
            print(f"\n[{r['id']}] {r['category']}")
            print(f"    Câu hỏi: {r['question']}")
            short_base = r['baseline'].replace('\n', ' ')[:100] + "..." if r['baseline'] else "N/A"
            short_react = str(r['react']).replace('\n', ' ')[:100] + "..." if r['react'] else "N/A"
            print(f"    Chatbot Baseline: {short_base}")
            print(f"    ReAct Agent:      {short_react}")
    else:
        try:
            test_id = int(choice)
            sample_test = next((t for t in tests if t["id"] == test_id), tests[0])
        except ValueError:
            sample_test = tests[0]
            
        sample_query = sample_test["question"]
        
        print(f"\nThực thi Test Case ID {sample_test.get('id')}: [{sample_test.get('category')}]")
        print("\n" + "="*20 + " DEMO 1: CHẠY TRÊN CHATBOT BASELINE " + "="*20)
        run_baseline_chatbot(sample_query, provider)
        
        print("\n" + "="*20 + " DEMO 2: CHẠY TRÊN REACT AGENT " + "="*20)
        run_react_agent(sample_query, provider)