"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề: Trợ Lý Tư Vấn Khóa Học Tiếng Anh (IELTS/TOEIC)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
"""

# =============================================================================
# 📚 DỮ LIỆU KHÓA HỌC MẪU (GIẢ LẬP DATABASE)
# =============================================================================
COURSES_DB = {
    "IELTS-BEG-01": {
        "course_id": "IELTS-BEG-01",
        "exam_type": "IELTS",
        "level": "Beginner",
        "name": "IELTS Beginner (0.0 - 4.0)",
        "price": 3500000,
        "duration_weeks": 8,
        "schedule": "Thứ 2 - 4 - 6, 18:00 - 20:00",
        "slots_available": 5,
    },
    "IELTS-INT-01": {
        "course_id": "IELTS-INT-01",
        "exam_type": "IELTS",
        "level": "Intermediate",
        "name": "IELTS Intermediate (4.0 - 5.5)",
        "price": 4500000,
        "duration_weeks": 10,
        "schedule": "Thứ 3 - 5 - 7, 18:00 - 20:00",
        "slots_available": 0,
    },
    "IELTS-ADV-01": {
        "course_id": "IELTS-ADV-01",
        "exam_type": "IELTS",
        "level": "Advanced",
        "name": "IELTS Advanced (5.5 - 7.0+)",
        "price": 5500000,
        "duration_weeks": 10,
        "schedule": "Thứ 7 - Chủ nhật, 08:00 - 11:00",
        "slots_available": 3,
    },
    "TOEIC-BEG-01": {
        "course_id": "TOEIC-BEG-01",
        "exam_type": "TOEIC",
        "level": "Beginner",
        "name": "TOEIC Beginner (0 - 350)",
        "price": 3000000,
        "duration_weeks": 6,
        "schedule": "Thứ 2 - 4 - 6, 19:00 - 21:00",
        "slots_available": 8,
    },
    "TOEIC-INT-01": {
        "course_id": "TOEIC-INT-01",
        "exam_type": "TOEIC",
        "level": "Intermediate",
        "name": "TOEIC Intermediate (350 - 650)",
        "price": 4000000,
        "duration_weeks": 8,
        "schedule": "Thứ 3 - 5 - 7, 19:00 - 21:00",
        "slots_available": 4,
    },
    "TOEIC-ADV-01": {
        "course_id": "TOEIC-ADV-01",
        "exam_type": "TOEIC",
        "level": "Advanced",
        "name": "TOEIC Advanced (650 - 900+)",
        "price": 4800000,
        "duration_weeks": 8,
        "schedule": "Chủ nhật, 08:00 - 12:00",
        "slots_available": 2,
        "promotion": "Giảm 10% khi đăng ký trước 15 ngày khai giảng",
    },
}


# =============================================================================
# 🛠️ CÁC HÀM CÔNG CỤ (TOOLS FOR REACT AGENT)
# =============================================================================

def search_courses(exam_type: str, level: str = None) -> str:
    """
    Tìm danh sách khóa học theo kỳ thi (IELTS/TOEIC) và trình độ (level).

    Args:
        exam_type (str): Loại kỳ thi ('IELTS' hoặc 'TOEIC')
level (str, optional): Trình độ ('Beginner', 'Intermediate', 'Advanced')

    Returns:
        str: Danh sách khóa học phù hợp (course_id, tên khóa) hoặc thông báo lỗi
    """
    try:
        exam_type_norm = exam_type.strip().upper()
        if exam_type_norm not in ("IELTS", "TOEIC"):
            return f"LỖI: Trung tâm chỉ đào tạo IELTS và TOEIC, không có kỳ thi '{exam_type}'."

        results = [
            c for c in COURSES_DB.values()
            if c["exam_type"] == exam_type_norm
            and (level is None or level == "" or c["level"].lower() == level.strip().lower())
        ]

        if not results:
            return f"LỖI: Không tìm thấy khóa {exam_type_norm} nào ở level '{level}'."

        lines = [f"- {c['course_id']}: {c['name']}" for c in results]
        return "Danh sách khóa học phù hợp:\n" + "\n".join(lines)
    except Exception as e:
        return f"LỖI HỆ THỐNG khi tìm kiếm khóa học: {str(e)}"


def get_course_detail(course_id: str) -> str:
    """
    Lấy thông tin chi tiết của một khóa học.

    Args:
        course_id (str): Mã khóa học (Ví dụ: 'IELTS-INT-01')

    Returns:
        str: Chi tiết khóa học (giá, thời lượng, lịch học) hoặc thông báo lỗi
    """
    try:
        cid_norm = course_id.strip().upper()
        course = COURSES_DB.get(cid_norm)
        if course is None:
            return f"LỖI: Không tìm thấy khóa học với mã '{course_id}'."

        return (
            f"📌 [{course['course_id']}] {course['name']}\n"
            f"- Học phí: {course['price']:,} VNĐ\n"
            f"- Thời lượng: {course['duration_weeks']} tuần\n"
            f"- Lịch học: {course['schedule']}\n"
            f"- Số chỗ còn trống: {course['slots_available']}"
        )
    except Exception as e:
        return f"LỖI HỆ THỐNG khi xem chi tiết khóa học: {str(e)}"


def suggest_level(exam_type: str, current_score: float) -> str:
    """
    Gợi ý trình độ (level) khóa học phù hợp dựa trên điểm số hiện tại của học viên.

    Args:
        exam_type (str): Loại kỳ thi ('IELTS' hoặc 'TOEIC')
        current_score (float): Điểm số hiện tại của học viên (Ví dụ: 4.5 hoặc '4.5')

    Returns:
        str: Level gợi ý ('Beginner', 'Intermediate', 'Advanced') hoặc thông báo lỗi
    """
    try:
        # Ép kiểu float phòng trường hợp LLM truyền string
        score = float(current_score)
    except (ValueError, TypeError):
        return f"LỖI: Điểm số '{current_score}' không hợp lệ, vui lòng nhập dạng số."

    try:
        exam_type_norm = exam_type.strip().upper()

        if exam_type_norm == "IELTS":
            if not (0.0 <= score <= 9.0):
                return f"LỖI: Điểm IELTS '{score}' không hợp lệ (phải trong khoảng 0.0 - 9.0)."
            if score < 4.0:
                level = "Beginner"
            elif score < 5.5:
                level = "Intermediate"
            else:
                level = "Advanced"
        elif exam_type_norm == "TOEIC":
            if not (0 <= score <= 990):
                return f"LỖI: Điểm TOEIC '{score}' không hợp lệ (phải trong khoảng 0 - 990)."
            if score < 350:
                level = "Beginner"
            elif score < 650:
                level = "Intermediate"
            else:
                level = "Advanced"
        else:
            return f"LỖI: Trung tâm chỉ đào tạo IELTS và TOEIC, không có kỳ thi '{exam_type}'."

        return f"Với điểm {exam_type_norm} hiện tại là {score}, level phù hợp là: {level}."
    except Exception as e:
        return f"LỖI HỆ THỐNG khi gợi ý level: {str(e)}"


def check_schedule(course_id: str) -> str:
    """
    Kiểm tra lịch học và tình trạng chỗ trống của một khóa học.

    Args:
        course_id (str): Mã khóa học (Ví dụ: 'IELTS-INT-01')

    Returns:
        str: Lịch học và số chỗ còn trống hoặc thông báo lỗi
    """
    try:
        cid_norm = course_id.strip().upper()
        course = COURSES_DB.get(cid_norm)
        if course is None:
            return f"LỖI: Không tìm thấy khóa học với mã '{course_id}'."

        if course["slots_available"] <= 0:
            return f"Khóa {course['name']} lịch học: {course['schedule']}. Hiện đã hết chỗ trống (0 chỗ)."

        return (
            f"Khóa {course['name']} lịch học: {course['schedule']}. "
            f"Còn {course['slots_available']} chỗ trống."
        )
    except Exception as e:
        return f"LỖI HỆ THỐNG khi kiểm tra lịch học: {str(e)}"


def compare_courses(course_ids) -> str:
    """
    So sánh giá và thời lượng giữa nhiều khóa học.

    Args:
        course_ids (list hoặc str): Danh sách mã khóa học cần so sánh (Ví dụ: ['IELTS-BEG-01', 'IELTS-INT-01'] hoặc 'IELTS-BEG-01, IELTS-INT-01')

    Returns:
        str: Bảng so sánh giá/thời lượng hoặc thông báo lỗi
    """
    try:
        # Xử lý linh hoạt nếu truyền dạng string phân cách dấu phẩy hoặc list
        if isinstance(course_ids, str):
            cids = [c.strip().upper() for c in course_ids.split(",") if c.strip()]
        elif isinstance(course_ids, list):
            cids = [str(c).strip().upper() for c in course_ids]
        else:
            cids = []

        if not cids or len(cids) < 2:
            return "LỖI: Cần ít nhất 2 mã khóa học hợp lệ để so sánh."

        lines = []
        for cid in cids:
            course = COURSES_DB.get(cid)
            if course is None:
                return f"LỖI: Không tìm thấy khóa học với mã '{cid}'."
            lines.append(
f"- [{course['course_id']}] {course['name']}: {course['price']:,} VNĐ, thời lượng {course['duration_weeks']} tuần"
            )

        return "So sánh các khóa học:\n" + "\n".join(lines)
    except Exception as e:
        return f"LỖI HỆ THỐNG khi so sánh khóa học: {str(e)}"


def calculate_price(course_id: str, has_promotion: bool = False) -> str:
    """
    Tính học phí cuối cùng của khóa học, áp dụng khuyến mãi nếu có.

    Args:
        course_id (str): Mã khóa học (Ví dụ: 'TOEIC-ADV-01')
        has_promotion (bool, optional): Có muốn kiểm tra/áp khuyến mãi hay không (True/False hoặc 'true')

    Returns:
        str: Học phí cuối cùng (đã áp khuyến mãi nếu có) hoặc thông báo lỗi
    """
    try:
        cid_norm = course_id.strip().upper()
        course = COURSES_DB.get(cid_norm)
        if course is None:
            return f"LỖI: Không tìm thấy khóa học với mã '{course_id}'."

        base_price = course["price"]
        
        # Ép kiểu boolean nếu truyền string
        is_promo = str(has_promotion).lower() in ("true", "1", "yes")

        if is_promo and "promotion" in course:
            discounted_price = int(base_price * 0.9)
            return (
                f"Học phí gốc khóa {course['name']}: {base_price:,} VNĐ.\n"
                f"Khuyến mãi: {course['promotion']}.\n"
                f"Học phí sau khuyến mãi (giảm 10%): {discounted_price:,} VNĐ."
            )

        return f"Học phí khóa {course['name']}: {base_price:,} VNĐ (hiện không áp dụng khuyến mãi)."
    except Exception as e:
        return f"LỖI HỆ THỐNG khi tính học phí: {str(e)}"


# =============================================================================
# 📋 REGISTRY ĐĂNG KÝ TOOL
# =============================================================================
AVAILABLE_TOOLS = {
    "search_courses": search_courses,
    "get_course_detail": get_course_detail,
    "suggest_level": suggest_level,
    "check_schedule": check_schedule,
    "compare_courses": compare_courses,
    "calculate_price": calculate_price,
}
