# 🏥 AI Agent Trợ Lý Dinh Dưỡng & Lối Sống Theo Bệnh Lý

## Phân tích chuyên sâu: Problem → Persona → AI Leverage

---

## 🔍 ĐỌC ĐỀ BÀI — RAW UNDERSTANDING

**Tên đề:** Hệ thống y tế X – AI Agent Trợ Lý Dinh Dưỡng & Lối Sống Theo Bệnh Lý

**Tech stack đề gợi ý:**

- LLM + LangGraph (orchestration: truy vấn thực phẩm → lập thực đơn → theo dõi)
- RAG trên bảng thành phần thực phẩm VN + Vector DB
- Food nutrition calculator / meal planner / food log
- Allergy & drug-food interaction checker
- Guardrails (chống hallucination số, kiểm chỉ định y khoa)
- Backend: FastAPI | Frontend: Next.js

**Vai trò:** Bệnh nhân & Chuyên gia Dinh dưỡng

---

## 🔴 PHẦN 1 — PROBLEM ANALYSIS (Vấn đề thực sự là gì?)

### 1.1 Thực trạng gốc rễ (Root Cause)

```
Bệnh nhân mắc bệnh lý mạn tính (tiểu đường, tim mạch, gout...)
        ↓
CẦN: chế độ ăn cực kỳ cụ thể & cá nhân hoá theo bệnh lý
        ↓
THỰC TẾ: Không thể tự lập thực đơn đúng về mặt lâm sàng
        ↓
KẾT QUẢ: Tuân theo lời khuyên thiếu căn cứ khoa học → nguy hiểm sức khoẻ
```

### 1.2 Phân tầng vấn đề (Problem Layers)

| Layer | Vấn đề cụ thể | Hệ quả |
|---|---|---|
| Kiến thức | Bệnh nhân không biết nguyên tắc dinh dưỡng lâm sàng | Ăn sai gây biến chứng |
| Công cụ | Không có tool tính toán kcal/chất dinh dưỡng theo hồ sơ cá nhân | Không theo dõi được |
| Hành vi | Không nhật ký ăn uống → không phản hồi điều chỉnh được | Mất kiểm soát |
| Tương tác | Tương tác thực phẩm-thuốc ít người biết | Nguy hiểm tiềm ẩn |
| Tin cậy | Lời khuyên từ internet không đáng tin, không nguồn gốc | Làm theo sai |
| Bảo mật | Dữ liệu y tế (PII/PHI) nhạy cảm | Nguy cơ rò rỉ |

### 1.3 Hard Constraints (Ràng buộc cứng — RẤT QUAN TRỌNG)

> **CAUTION**
> Đây là những giới hạn KHÔNG được vi phạm trong thiết kế AI:

- AI KHÔNG được tự đề chế độ ăn kiêng y khoa — phải dựa trên guideline chuyên gia dinh dưỡng
- KHÔNG hallucinate số — calorie, dinh dưỡng phải có nguồn từ CSDL thực phẩm VN chuẩn
- Phải cảnh báo tương tác thực phẩm-thuốc (drug-food interaction)
- Bảo vệ PII/PHI của bệnh nhân
- Luôn khuyến nghị tham vấn chuyên gia — AI là trợ lý, không phải bác sĩ

### 1.4 Problem Statement (1 câu cô đọng)

> "Bệnh nhân mắc bệnh mạn tính cần chế độ dinh dưỡng cá nhân hoá theo lâm sàng, nhưng thiếu công cụ đáng tin cậy để lập, theo dõi, và điều chỉnh thực đơn theo đúng chuẩn y tế — dẫn đến tuân thủ dinh dưỡng kém và nguy cơ biến chứng tăng."

---

## 👥 PHẦN 2 — PERSONA ANALYSIS (Ai đang dùng?)

### Persona 1: BỆNH NHÂN MẠN TÍNH

**👤 Nguyễn Thị Lan — Bệnh nhân tiểu đường Type 2, 58 tuổi**

**📍 Bối cảnh:**
- Vừa được chẩn đoán 6 tháng trước
- Đang dùng metformin + thuốc huyết áp
- Sống cùng gia đình, tự nấu ăn
- Không rành công nghệ lắm, dùng smartphone cơ bản

**🎯 Goals (Mục tiêu):**
- Kiểm soát đường huyết qua ăn uống
- Biết ăn gì hằng ngày mà không phải tính toán phức tạp
- Không ăn nhầm thứ tương tác xấu với thuốc
- Nhận thực đơn phù hợp nguyên liệu sẵn có ở chợ VN

**😤 Pain Points (Khó khăn):**
- Không biết GI (chỉ số đường huyết) của thực phẩm VN
- Mâu thuẫn giữa lời khuyên bác sĩ & bài đăng mạng xã hội
- Không theo dõi được đã ăn đủ/thừa/thiếu chất gì
- Sợ ăn nhầm gây biến chứng

**📱 Behaviours (Hành vi):**
- Chụp ảnh bữa ăn chia sẻ lên Facebook
- Hỏi con cái về thực phẩm tốt/xấu
- Dùng Zalo để nhắn tin với người thân
- Đi khám định kỳ 1-3 tháng/lần

### Persona 2: CHUYÊN GIA DINH DƯỠNG

**👤 BS. Phạm Minh Tuấn — Chuyên gia Dinh dưỡng, 35 tuổi**

**📍 Bối cảnh:**
- Làm việc tại bệnh viện, tư vấn 15-20 bệnh nhân/ngày
- Muốn theo dõi tuân thủ dinh dưỡng giữa các lần khám
- Có kiến thức chuyên môn, cần công cụ để scale tư vấn

**🎯 Goals:**
- Duyệt/chỉnh thực đơn AI đề xuất cho từng bệnh nhân
- Nhận cảnh báo khi bệnh nhân ăn lệch khuyến nghị
- Có data nhật ký ăn uống để phân tích trước khi khám
- Tin tưởng nguồn gốc dữ liệu dinh dưỡng AI dùng

**😤 Pain Points:**
- Không biết bệnh nhân có tuân thủ giữa các lần khám
- Mất nhiều thời gian lập thực đơn thủ công
- Lo ngại AI cho lời khuyên sai → trách nhiệm pháp lý
- Khó scale khi số bệnh nhân quản lý tăng

### Persona 3: NGƯỜI THÂN/NGƯỜI CHĂM SÓC (Secondary)

**👤 Con cái / vợ chồng — Người nấu ăn cho bệnh nhân**

- **Goals:** Biết nấu gì đúng cho người thân mắc bệnh
- **Pain:** Không biết thay thế nguyên liệu khi thiếu
- **→ Cần:** Danh sách đi chợ + gợi ý thay thế thực phẩm

### Persona Journey Map

**BỆNH NHÂN LAN — HÀNH TRÌNH SỬ DỤNG APP**

`[Onboarding] → [Nhập hồ sơ] → [Nhận thực đơn] → [Log bữa ăn] → [Nhận phản hồi] → [Tái khám]`

| Onboarding | Nhập hồ sơ | Nhận thực đơn | Log bữa ăn | Nhận phản hồi | Tái khám |
|---|---|---|---|---|---|
| — | Nhập bệnh lý, thuốc đang dùng, mục tiêu sức khoẻ | AI phân tích ràng buộc, giới hạn ăn kiêng | Thực đơn 7 ngày cá nhân hoá, có nguồn VN | Chụp ảnh/nhập thủ công, AI nhận diện & tính kcal | Cảnh báo nếu vượt ngưỡng, gợi ý điều chỉnh |
| — | — | — | — | — | Bác sĩ xem data nhật ký trước khi tư vấn |

---

## 🤖 PHẦN 3 — AI LEVERAGE (Leverage AI ở đâu & như thế nào?)

### 3.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI AGENT ORCHESTRATION (LangGraph)            │
│                                                                   │
│  [User Input] → [Intent Router] → [Tool Selector] → [Response]  │
│                                                                   │
│  Tools:                                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │  RAG DB  │ │ Meal     │ │ Food Log │ │ Drug-Food│           │
│  │  (VN food│ │ Planner  │ │ Tracker  │ │ Interact │           │
│  │  CSDL)   │ │ Tool     │ │ Tool     │ │ Checker  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│                                                                   │
│  Guardrails: Chống hallucinate số | Kiểm chỉ định y khoa        │
│  Memory: Hồ sơ bệnh nhân + lịch sử ăn uống                     │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 AI Leverage Points (9 điểm đòn bẩy AI)

#### 🔵 TIER 1 — CORE (Bắt buộc phải có)

| # | AI Leverage Point | Kỹ thuật | Tại sao quan trọng |
|---|---|---|---|
| 1 | RAG trên CSDL thực phẩm VN | Vector search trên bảng dinh dưỡng VN + WHO/AHA guidelines | Chống hallucinate, đảm bảo số liệu có nguồn gốc |
| 2 | Personalised Meal Planning | LLM + ràng buộc từ hồ sơ bệnh nhân (bệnh lý, thuốc, dị ứng, sở thích) | Tạo thực đơn 7 ngày phù hợp lâm sàng |
| 3 | Food Log & Nutrition Tracking | NLP + food recognition + nutrition calculator | Tự động phân tích bữa ăn đã ăn |
| 4 | Guardrails & Medical Safety | Rule-based + LLM validation | KHÔNG bao giờ vượt phạm vi y tế |

#### 🟡 TIER 2 — DIFFERENTIATION (Điểm khác biệt)

| # | AI Leverage Point | Kỹ thuật | Impact |
|---|---|---|---|
| 5 | Drug-Food Interaction Checker | Knowledge graph + RAG | Cảnh báo tương tác nguy hiểm ngay lập tức |
| 6 | Adaptive Feedback Loop | Memory + pattern analysis | Điều chỉnh thực đơn dựa trên thực tế ăn uống của user |
| 7 | Expert Review Workflow | Human-in-the-loop (BS duyệt thực đơn AI) | Tăng tin cậy y tế, giảm rủi ro pháp lý |

#### 🟢 TIER 3 — WOW FACTOR (Gây ấn tượng giám khảo)

| # | AI Leverage Point | Kỹ thuật | Impact |
|---|---|---|---|
| 8 | Multimodal Food Recognition | Vision model nhận diện thức ăn từ ảnh | UX đơn giản cho bệnh nhân lớn tuổi |
| 9 | Proactive Nutritional Alerts | Anomaly detection trên nutrition log | Cảnh báo thiếu/thừa chất trước khi có triệu chứng |

### 3.3 LangGraph Flow — Chi tiết

```
START
  │
  ▼
[ProfileLoader] — Load hồ sơ: bệnh lý, BMI, thuốc, dị ứng, mục tiêu
  │
  ▼
[IntentClassifier] — Phân loại yêu cầu:
  ├── "lập thực đơn" → MealPlannerAgent
  ├── "tôi vừa ăn..." → FoodLogAgent
  ├── "thuốc này ăn gì được?" → DrugFoodAgent
  └── "tôi thiếu/thừa chất?" → NutritionAnalysisAgent
  │
  ▼
[ToolExecutor]
  ├── RAGRetriever (CSDL thực phẩm VN + guidelines)
  ├── NutritionCalculator (tính kcal, macro, micro)
  ├── InteractionChecker (drug-food KB)
  └── MealOptimizer (LP/heuristic để balance thực đơn)
  │
  ▼
[GuardrailsValidator]
  ├── Kiểm tra: response có vượt phạm vi y tế không?
  ├── Kiểm tra: số liệu có nguồn từ RAG không?
  └── Nếu fail → redirect to "tham vấn chuyên gia"
  │
  ▼
[ResponseGenerator] — Trả lời với:
  ├── Thực đơn / phân tích có nguồn trích dẫn
  ├── Cảnh báo (nếu có)
  └── Gợi ý tham vấn BS (nếu cần)
  │
  ▼
[MemoryUpdater] — Lưu context: sở thích, lịch sử, phản hồi
  │
  ▼
END
```

### 3.4 RAG Strategy — Cụ thể

```
Data Sources cần index:
├── Bảng thành phần thực phẩm VN (Bộ Y Tế / Viện Dinh Dưỡng Quốc Gia)
├── Guidelines: ADA (đái tháo đường), AHA (tim mạch), ACR (gout)
├── Danh sách tương tác thực phẩm-thuốc
└── Thực đơn mẫu theo bệnh lý từ chuyên gia

Chunking strategy:
├── Food item: {tên, kcal/100g, protein, carb, fat, GI, minerals}
├── Guideline chunk: {bệnh lý, khuyến nghị, giới hạn, nguồn}
└── Interaction: {thuốc, thực phẩm, cơ chế, mức độ nguy hiểm}

Retrieval:
└── Hybrid search: Dense (semantic) + Sparse (BM25 tên thực phẩm VN)
    → Reranker → Top-K → LLM synthesis
```

### 3.5 Điểm khác biệt vs. App dinh dưỡng thông thường

| Tính năng | App thông thường (MyFitnessPal...) | App này |
|---|---|---|
| Dữ liệu thực phẩm | CSDL quốc tế (thiếu thực phẩm VN) | CSDL VN chuẩn Bộ Y Tế |
| Cá nhân hoá | Theo mục tiêu (giảm cân, tăng cơ) | Theo bệnh lý lâm sàng cụ thể |
| AI Role | Tracker đơn thuần | Conversational Agent + RAG |
| Bác sĩ/chuyên gia | Không | Human-in-the-loop review |
| Drug interaction | Không | Có — cảnh báo thực phẩm-thuốc |
| Guardrails y tế | Không | Có — không vượt phạm vi lâm sàng |
| Nguồn trích dẫn | Không | Có — mọi khuyến nghị đều có nguồn |

---

## 🎯 PHẦN 4 — CHIẾN LƯỢC TRIỂN KHAI

### 4.1 MVP Scope (Tối thiểu để thắng)

**✅ PHẢI CÓ (Pass Hard Constraints):**
1. Hồ sơ bệnh nhân: bệnh lý + thuốc + dị ứng + mục tiêu
2. Thực đơn 7 ngày tự động theo hồ sơ (có nguồn từ CSDL VN)
3. Food log: nhập bằng text/search (không cần vision cho MVP)
4. Cảnh báo vượt ngưỡng kcal/chất
5. Drug-food interaction checker cơ bản
6. Guardrails: luôn ghi nguồn + redirect bác sĩ khi cần
7. Vai trò BS duyệt thực đơn

**⭐ NÊN CÓ (Thắng điểm cao):**
8. Food recognition từ ảnh (multimodal)
9. Memory: nhớ sở thích, thực phẩm hay dùng
10. Danh sách đi chợ tự động
11. Adaptive plan: điều chỉnh theo log thực tế

### 4.2 Killer Demo Script

**SCENARIO: Bệnh nhân tiểu đường hỏi về bữa sáng**

> **User:** "Tôi muốn ăn cháo trắng với trứng sáng nay được không?"

**AI:**
```
├── [RAGRetriever] → GI của cháo trắng = 78 (cao), phù hợp giới hạn không?
├── [ProfileCheck] → HbA1c bệnh nhân đang cao, giới hạn carb = 45g/bữa
├── [DrugCheck] → metformin + trứng: OK, không tương tác
├── [NutritionCalc] → cháo trắng 1 tô = 35g carb + trứng = OK trong giới hạn
└── [Response]:
    "Được! Cháo trắng có GI cao (78), nhưng 1 tô nhỏ (~200ml) + 1 trứng luộc
    chỉ khoảng 35g carb, nằm trong giới hạn của bạn. Gợi ý: thêm rau luộc
    để giảm tốc độ hấp thu đường. [Nguồn: CSDL thực phẩm VN - Viện DD 2020]"
```

---

## 📋 PHẦN 5 — SUMMARY & NEXT STEPS

### Một câu tóm tắt giá trị (Value Proposition)

> "AI Agent dinh dưỡng đầu tiên dành cho bệnh nhân mạn tính Việt Nam — cá nhân hoá theo bệnh lý, có nguồn y tế đáng tin, kết nối chuyên gia dinh dưỡng — không bao giờ tự đặt chẩn đoán."

### Điểm mạnh khi pitch

| Điểm | Lý do thuyết phục |
|---|---|
| Safety First | Guardrails + human-in-the-loop → giải quyết lo ngại y tế |
| Vietnam-First | CSDL thực phẩm VN thực tế, không phải thực phẩm Tây |
| Clinically Grounded | RAG từ guidelines chuẩn → không hallucinate |
| Dual Value | Tốt cho bệnh nhân VÀ cho BS (data trước tái khám) |
| Scalable Trust | BS duyệt → tăng adoption trong hệ thống y tế |

### Next Steps đề xuất

- [ ] Xây dựng CSDL thực phẩm VN — scrape + clean từ Viện Dinh Dưỡng Quốc Gia
- [ ] Thiết kế schema hồ sơ bệnh nhân — fields cần thiết cho từng bệnh lý
- [ ] Prototype LangGraph flow — test với 3 intent: lập thực đơn, food log, interaction check
- [ ] Xây dựng Guardrails rules — list các câu AI phải redirect sang BS
- [ ] Design UI/UX — đặc biệt onboarding & food logging (thân thiện với người lớn tuổi)
- [ ] Pilot với 1 bệnh lý — đề xuất: Tiểu đường Type 2 (phổ biến nhất, guideline rõ ràng)
