# 🛠️ ROLE 2: DANH SÁCH & THIẾT KẾ CÔNG CỤ (TOOL SPECIFICATIONS)

> **Chủ đề dự án**: Trợ Lý Tư Vấn Khóa Học IELTS & TOEIC  
> **Người thực hiện**: Role 2 - Tool & Spec Engineer  
> **File triển khai code**: `src/tools.py`

---

## 📋 1. BẢNG TỔNG HỢP DANH SÁCH 6 CÔNG CỤ (TOOL REGISTRY)

| STT | Tên Tool (Function) | Tham số (Parameters) | Mô tả ngắn |
| :---: | :--- | :--- | :--- |
| 1 | `suggest_level` | `exam_type: str, current_score: str` | Gợi ý level khóa học phù hợp dựa trên điểm thi test đầu vào |
| 2 | `search_courses` | `query: str, level: str = ""` | Tìm kiếm khóa học theo từ khóa (`IELTS`, `TOEIC`, `Cấp tốc`,...) hoặc level |
| 3 | `get_course_detail` | `course_id: str` | Trả về thông tin chi tiết: tên khóa, giá gốc, thời lượng, giáo viên, đầu ra |
| 4 | `check_schedule` | `course_id: str` | Tra cứu lịch học cụ thể (ngày, giờ) và tình trạng sĩ số/chỗ trống |
| 5 | `compare_courses` | `course_ids_str: str` | So sánh giá & thời lượng giữa nhiều khóa học (phân cách bằng dấu phẩy) |
| 6 | `calculate_price` | `course_id: str, promo_code: str = ""` | Tính tổng tiền học phí sau khi áp mã ưu đãi / khuyến mãi (nếu có) |

---

## 🔍 2. CHI TIẾT SPEC CÁC CÔNG CỤ & DOCSTRINGS

### 1️⃣ `suggest_level`
* **Mục đích**: Phân tích điểm hiện tại của học viên để đề xuất cấp độ học phù hợp.
* **Docstring**:
  ```python
  def suggest_level(exam_type: str, current_score: str) -> str:
      """
      Gợi ý cấp độ khóa học phù hợp dựa trên bài test đầu vào hoặc điểm hiện tại.
      
      Args:
          exam_type (str): Loại kỳ thi ('IELTS' hoặc 'TOEIC')
          current_score (str): Điểm hiện tại (Ví dụ: '4.5' đối với IELTS, '450' đối với TOEIC)
          
      Returns:
          str: Đề xuất cấp độ học (Beginner, Intermediate, Advanced) và gợi ý khóa học tiếp theo.
      """
  ```
* **Xử lý lỗi**: Trả về `"LỖI: exam_type phải là 'IELTS' hoặc 'TOEIC'"` nếu truyền sai loại kỳ thi.

---

### 2️⃣ `search_courses`
* **Mục đích**: Tìm kiếm danh sách các khóa học theo nhu cầu người dùng.
* **Docstring**:
  ```python
  def search_courses(query: str, level: str = "") -> str:
      """
      Tìm kiếm các khóa học tiếng Anh theo từ khóa nhu cầu hoặc cấp độ.
      
      Args:
          query (str): Từ khóa tìm kiếm (Ví dụ: 'IELTS', 'TOEIC', 'Cấp tốc', 'Buổi tối')
          level (str, optional): Cấp độ khóa học ('Beginner', 'Intermediate', 'Advanced')
          
      Returns:
          str: Danh sách mã khóa học và tên khóa học thỏa mãn điều kiện.
      """
  ```
* **Xử lý lỗi**: Trả về `"LỖI: Không tìm thấy khóa học nào phù hợp với từ khóa '{query}'"`.

---

### 3️⃣ `get_course_detail`
* **Mục đích**: Tra cứu toàn bộ thông tin chi tiết của 1 khóa học cụ thể.
* **Docstring**:
  ```python
  def get_course_detail(course_id: str) -> str:
      """
      Tra cứu thông tin chi tiết của một khóa học theo mã khóa học.
      
      Args:
          course_id (str): Mã khóa học (Ví dụ: 'IELTS_INTER', 'TOEIC_750')
          
      Returns:
          str: Chi tiết tên khóa, giá gốc, thời lượng, giảng viên, đầu ra cam kết.
      """
  ```
* **Xử lý lỗi**: Trả về `"LỖI: Không tồn tại mã khóa học '{course_id}' trong hệ thống"`.

---

### 4️⃣ `check_schedule`
* **Mục đích**: Kiểm tra lịch học và số chỗ trống còn lại.
* **Docstring**:
  ```python
  def check_schedule(course_id: str) -> str:
      """
      Tra cứu thời khóa biểu và số chỗ trống khả dụng của khóa học.
      
      Args:
          course_id (str): Mã khóa học (Ví dụ: 'IELTS_INTER')
          
      Returns:
          str: Lịch học (thứ, giờ) và số ghế trống còn lại.
      """
  ```
* **Xử lý lỗi**: Trả về `"LỖI: Không tìm thấy lịch học cho mã khóa '{course_id}'"`.

---

### 5️⃣ `compare_courses`
* **Mục đích**: Đặt lên bàn cân 2 hoặc nhiều khóa học để người dùng dễ lựa chọn.
* **Docstring**:
  ```python
  def compare_courses(course_ids_str: str) -> str:
      """
      So sánh học phí, thời lượng và cam kết đầu ra giữa nhiều khóa học.
      
      Args:
          course_ids_str (str): Các mã khóa học phân cách bằng dấu phẩy (Ví dụ: 'IELTS_BEGIN, IELTS_INTER')
          
      Returns:
          str: Bảng hoặc danh sách so sánh đối chiếu giữa các khóa.
      """
  ```
* **Xử lý lỗi**: Trả về `"LỖI: Cần cung cấp ít nhất 2 mã khóa học hợp lệ để so sánh"`.

---

### 6️⃣ `calculate_price`
* **Mục đích**: Tính toán học phí thực tế sau khi áp mã giảm giá / ưu đãi sinh viên.
* **Docstring**:
  ```python
  def calculate_price(course_id: str, promo_code: str = "") -> str:
      """
      Tính tổng học phí phải nộp cho khóa học sau khi áp dụng mã giảm giá.
      
      Args:
          course_id (str): Mã khóa học (Ví dụ: 'IELTS_INTER')
          promo_code (str, optional): Mã ưu đãi (Ví dụ: 'SV2026', 'SUMMER10')
          
      Returns:
          str: Học phí gốc, số tiền được giảm và tổng chi phí thanh toán cuối cùng.
      """
  ```
* **Xử lý lỗi**: Trả về thông báo nếu mã `promo_code` bị hết hạn hoặc không tồn tại, vẫn trả về giá gốc thay vì crash code.

---

## 🛡️ 3. NGUYÊN TẮC AN TOÀN & CHỊU LỖI (SAFEGUARDS / ERROR HANDLING)

Theo đúng yêu cầu của **Mốc 3**, tất cả 6 công cụ trên cam kết tuân thủ quy tắc:
1. **Không ném ngoại lệ (No Uncaught Exception)**: Bao bọc bằng `try...except`.
2. **Trả về chuỗi văn bản thông báo lỗi (String Error Output)**: Giúp ReAct Agent đọc được lỗi ở bước `Observation` và đưa ra phản hồi lịch sự cho người dùng.
