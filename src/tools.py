"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề: Trợ Lý Tư Vấn Khóa Học Tiếng Anh (IELTS & TOEIC)
File code được chuẩn hóa chính xác theo spec trong docs/role2_tools_spec.md
"""

# =============================================================================
# 📚 DỮ LIỆU KHÓA HỌC MẪU (MOCK DATABASE)
# =============================================================================
COURSES_DB = {
    "IELTS_BEGIN": {
        "course_id": "IELTS_BEGIN",
        "exam_type": "IELTS",
        "level": "Beginner",
        "name": "IELTS Nền Tảng (0.0 - 4.0)",
        "price": 3500000,
        "duration_weeks": 8,
        "schedule": "Thứ 2 - 4 - 6 (18:00 - 20:00)",
        "slots_available": 5,
        "teacher": "ThS. Nguyễn Văn A (IELTS 8.5)",
        "commitment": "Đầu ra Cam kết IELTS 4.0+",
        "description": "Dành cho người mất gốc, củng cố ngữ pháp, từ vựng và phát âm chuẩn."
    },
    "IELTS_INTER": {
        "course_id": "IELTS_INTER",
        "exam_type": "IELTS",
        "level": "Intermediate",
        "name": "IELTS Bứt Phá (4.0 - 5.5)",
        "price": 4500000,
        "duration_weeks": 10,
        "schedule": "Thứ 3 - 5 - 7 (18:00 - 20:00)",
        "slots_available": 0,
        "teacher": "Cô Trần Thị B (IELTS 8.0)",
        "commitment": "Đầu ra Cam kết IELTS 5.5+",
        "description": "Luyện kỹ năng làm bài 4 kỹ năng Nghe - Nói - Đọc - Viết cấp độ trung cấp."
    },
    "IELTS_ADV": {
        "course_id": "IELTS_ADV",
        "exam_type": "IELTS",
        "level": "Advanced",
        "name": "IELTS Chinh Phục (5.5 - 7.0+)",
        "price": 5500000,
        "duration_weeks": 10,
        "schedule": "Thứ 7 - Chủ nhật (08:00 - 11:00)",
        "slots_available": 3,
        "teacher": "Thầy John Smith (Native Speaker)",
        "commitment": "Đầu ra Cam kết IELTS 7.0+",
        "description": "Chiến thuật nâng Band điểm thần tốc, sửa bài Writing/Speaking 1-1."
    },
    "TOEIC_BEGIN": {
        "course_id": "TOEIC_BEGIN",
        "exam_type": "TOEIC",
        "level": "Beginner",
        "name": "TOEIC Cơ Bản (0 - 350)",
        "price": 3000000,
        "duration_weeks": 6,
        "schedule": "Thứ 2 - 4 - 6 (19:00 - 21:00)",
        "slots_available": 8,
        "teacher": "Thầy Lê Văn C (TOEIC 950)",
        "commitment": "Đầu ra Cam kết TOEIC 350+",
        "description": "Xây dựng nền tảng từ vựng TOEIC căn bản và ngữ pháp bắt buộc."
    },
    "TOEIC_INTER": {
        "course_id": "TOEIC_INTER",
        "exam_type": "TOEIC",
        "level": "Intermediate",
        "name": "TOEIC Mục Tiêu 650 (350 - 650)",
        "price": 4000000,
        "duration_weeks": 8,
        "schedule": "Thứ 3 - 5 - 7 (19:00 - 21:00)",
        "slots_available": 4,
        "teacher": "Cô Phạm Thị D (TOEIC 990)",
        "commitment": "Đầu ra Cam kết TOEIC 650+",
        "description": "Luyện đề TOEIC Part 1-7, mẹo tránh bẫy câu hỏi đọc và nghe."
    },
    "TOEIC_ADV": {
        "course_id": "TOEIC_ADV",
        "exam_type": "TOEIC",
        "level": "Advanced",
        "name": "TOEIC Nâng Cao (650 - 900+)",
        "price": 4800000,
        "duration_weeks": 8,
        "schedule": "Chủ nhật (08:00 - 12:00)",
        "slots_available": 2,
        "teacher": "Thầy Hoàng Anh (TOEIC 990)",
        "commitment": "Đầu ra Cam kết TOEIC 900+",
        "description": "Luyện đề cường độ cao, chiến thuật làm bài Part 7 đọc hiểu dài."
    }
}

# Alias mapping cho các mã cũ nếu có (ví dụ: 'IELTS-INT-01' -> 'IELTS_INTER')
ALIAS_MAP = {
    "IELTS-BEG-01": "IELTS_BEGIN",
    "IELTS-INT-01": "IELTS_INTER",
    "IELTS-ADV-01": "IELTS_ADV",
    "TOEIC-BEG-01": "TOEIC_BEGIN",
    "TOEIC-INT-01": "TOEIC_INTER",
    "TOEIC-ADV-01": "TOEIC_ADV",
}

# Mã giảm giá giả lập
PROMO_CODES = {
    "SV2026": {"discount_percent": 15, "description": "Ưu đãi Sinh viên 2026 (-15%)"},
    "SUMMER10": {"discount_percent": 10, "description": "Ưu đãi Chào Hè (-10%)"},
}


def _get_course(course_id: str):
    """Helper lấy course từ ID hoặc Alias"""
    if not course_id:
        return None
    cid_upper = course_id.strip().upper()
    real_id = ALIAS_MAP.get(cid_upper, cid_upper)
    return COURSES_DB.get(real_id)


# =============================================================================
# 🛠️ CHUẨN HÓA 6 TOOLS THEO ĐÚNG DOCS/ROLE2_TOOLS_SPEC.MD
# =============================================================================

def suggest_level(exam_type: str, current_score: str) -> str:
    """
    Gợi ý cấp độ khóa học phù hợp dựa trên bài test đầu vào hoặc điểm hiện tại.
    
    Args:
        exam_type (str): Loại kỳ thi ('IELTS' hoặc 'TOEIC')
        current_score (str): Điểm hiện tại (Ví dụ: '4.5' đối với IELTS, '450' đối với TOEIC)
        
    Returns:
        str: Đề xuất cấp độ học (Beginner, Intermediate, Advanced) và gợi ý khóa học tiếp theo.
    """
    try:
        exam_norm = str(exam_type).strip().upper()
        if exam_norm not in ("IELTS", "TOEIC"):
            return "LỖI: exam_type phải là 'IELTS' hoặc 'TOEIC'"

        try:
            score = float(str(current_score).strip())
        except (ValueError, TypeError):
            return f"LỖI: Điểm hiện tại '{current_score}' phải là số hợp lệ (Ví dụ: '4.5' hoặc '450')."

        if exam_norm == "IELTS":
            if not (0.0 <= score <= 9.0):
                return f"LỖI: Điểm IELTS '{score}' không hợp lệ (phải từ 0.0 đến 9.0)."
            if score < 4.0:
                level = "Beginner"
                suggested_course = "IELTS_BEGIN (IELTS Nền Tảng)"
            elif score < 5.5:
                level = "Intermediate"
                suggested_course = "IELTS_INTER (IELTS Bứt Phá)"
            else:
                level = "Advanced"
                suggested_course = "IELTS_ADV (IELTS Chinh Phục)"
        else:  # TOEIC
            if not (0 <= score <= 990):
                return f"LỖI: Điểm TOEIC '{score}' không hợp lệ (phải từ 0 đến 990)."
            if score < 350:
                level = "Beginner"
                suggested_course = "TOEIC_BEGIN (TOEIC Cơ Bản)"
            elif score < 650:
                level = "Intermediate"
                suggested_course = "TOEIC_INTER (TOEIC Mục Tiêu 650)"
            else:
                level = "Advanced"
                suggested_course = "TOEIC_ADV (TOEIC Nâng Cao)"

        return (
            f"🎯 Dựa trên điểm {exam_norm} hiện tại là {score}, cấp độ phù hợp của bạn là: **{level}**.\n"
            f"💡 Khóa học gợi ý tiếp theo: {suggested_course}."
        )
    except Exception as e:
        return f"LỖI HỆ THỐNG khi gợi ý level: {str(e)}"


def search_courses(query: str, level: str = "") -> str:
    """
    Tìm kiếm các khóa học tiếng Anh theo từ khóa nhu cầu hoặc cấp độ.
    
    Args:
        query (str): Từ khóa tìm kiếm (Ví dụ: 'IELTS', 'TOEIC', 'Cấp tốc', 'Buổi tối')
        level (str, optional): Cấp độ khóa học ('Beginner', 'Intermediate', 'Advanced')
        
    Returns:
        str: Danh sách mã khóa học và tên khóa học thỏa mãn điều kiện.
    """
    try:
        q_lower = str(query).strip().lower()
        lvl_lower = str(level).strip().lower()

        matched = []
        for cid, info in COURSES_DB.items():
            # Check match query trong ID, exam_type, name, schedule, description
            text_corpus = f"{cid} {info['exam_type']} {info['name']} {info['schedule']} {info['description']}".lower()
            
            match_query = (q_lower in text_corpus)
            match_level = (not lvl_lower or lvl_lower in info['level'].lower())
            
            if match_query and match_level:
                matched.append(f"- [{info['course_id']}] {info['name']} ({info['exam_type']} - Level: {info['level']})")

        if matched:
            return f"Danh sách khóa học phù hợp với từ khóa '{query}':\n" + "\n".join(matched)
        else:
            return f"LỖI: Không tìm thấy khóa học nào phù hợp với từ khóa '{query}'"
    except Exception as e:
        return f"LỖI HỆ THỐNG khi tìm kiếm khóa học: {str(e)}"


def get_course_detail(course_id: str) -> str:
    """
    Tra cứu thông tin chi tiết của một khóa học theo mã khóa học.
    
    Args:
        course_id (str): Mã khóa học (Ví dụ: 'IELTS_INTER', 'TOEIC_750')
        
    Returns:
        str: Chi tiết tên khóa, giá gốc, thời lượng, giảng viên, đầu ra cam kết.
    """
    try:
        course = _get_course(course_id)
        if not course:
            return f"LỖI: Không tồn tại mã khóa học '{course_id}' trong hệ thống"

        return (
            f"📌 Chi tiết khóa học [{course['course_id']}]: {course['name']}\n"
            f"- Cấp độ: {course['level']} ({course['exam_type']})\n"
            f"- Học phí gốc: {course['price']:,} VNĐ\n"
            f"- Thời lượng: {course['duration_weeks']} tuần\n"
            f"- Giảng viên: {course['teacher']}\n"
            f"- Lịch học: {course['schedule']}\n"
            f"- Cam kết đầu ra: {course['commitment']}\n"
            f"- Mô tả: {course['description']}"
        )
    except Exception as e:
        return f"LỖI HỆ THỐNG khi xem chi tiết khóa học: {str(e)}"


def check_schedule(course_id: str) -> str:
    """
    Tra cứu thời khóa biểu và số chỗ trống khả dụng của khóa học.
    
    Args:
        course_id (str): Mã khóa học (Ví dụ: 'IELTS_INTER')
        
    Returns:
        str: Lịch học (thứ, giờ) và số ghế trống còn lại.
    """
    try:
        course = _get_course(course_id)
        if not course:
            return f"LỖI: Không tìm thấy lịch học cho mã khóa '{course_id}'"

        slots = course["slots_available"]
        slot_status = f"Còn {slots} chỗ trống" if slots > 0 else "HẾT CHỖ TRỐNG"

        return (
            f"🗓️ Lịch học khóa [{course['course_id']}] ({course['name']}):\n"
            f"- Thời gian: {course['schedule']}\n"
            f"- Tình trạng sĩ số: {slot_status}"
        )
    except Exception as e:
        return f"LỖI HỆ THỐNG khi kiểm tra lịch học: {str(e)}"


def compare_courses(course_ids_str: str) -> str:
    """
    So sánh học phí, thời lượng và cam kết đầu ra giữa nhiều khóa học.
    
    Args:
        course_ids_str (str): Các mã khóa học phân cách bằng dấu phẩy (Ví dụ: 'IELTS_BEGIN, IELTS_INTER')
        
    Returns:
        str: Bảng hoặc danh sách so sánh đối chiếu giữa các khóa.
    """
    try:
        # Hỗ trợ truyền dạng chuỗi 'IELTS_BEGIN, IELTS_INTER' hoặc list
        if isinstance(course_ids_str, list):
            raw_ids = course_ids_str
        else:
            raw_ids = str(course_ids_str).split(",")

        cids = [c.strip().upper() for c in raw_ids if c.strip()]

        if len(cids) < 2:
            return "LỖI: Cần cung cấp ít nhất 2 mã khóa học hợp lệ để so sánh"

        courses = []
        for cid in cids:
            course = _get_course(cid)
            if not course:
                return f"LỖI: Không tồn tại mã khóa học '{cid}' trong hệ thống"
            courses.append(course)

        lines = ["⚖️ SO SÁNH CÁC KHÓA HỌC:"]
        for c in courses:
            lines.append(
                f"- [{c['course_id']}] {c['name']}:\n"
                f"  + Học phí: {c['price']:,} VNĐ | Thời lượng: {c['duration_weeks']} tuần\n"
                f"  + Lịch học: {c['schedule']}\n"
                f"  + Cam kết: {c['commitment']}"
            )

        return "\n".join(lines)
    except Exception as e:
        return f"LỖI HỆ THỐNG khi so sánh khóa học: {str(e)}"


def calculate_price(course_id: str, promo_code: str = "") -> str:
    """
    Tính tổng học phí phải nộp cho khóa học sau khi áp dụng mã giảm giá.
    
    Args:
        course_id (str): Mã khóa học (Ví dụ: 'IELTS_INTER')
        promo_code (str, optional): Mã ưu đãi (Ví dụ: 'SV2026', 'SUMMER10')
        
    Returns:
        str: Học phí gốc, số tiền được giảm và tổng chi phí thanh toán cuối cùng.
    """
    try:
        course = _get_course(course_id)
        if not course:
            return f"LỖI: Không tồn tại mã khóa học '{course_id}' trong hệ thống"

        base_price = course["price"]
        code_upper = str(promo_code).strip().upper()

        if not code_upper:
            return (
                f"💰 Học phí khóa [{course['course_id']}] {course['name']}:\n"
                f"- Giá gốc: {base_price:,} VNĐ\n"
                f"- Mã ưu đãi: Không áp dụng\n"
                f"- Tổng chi phí thanh toán: {base_price:,} VNĐ"
            )

        if code_upper in PROMO_CODES:
            promo_info = PROMO_CODES[code_upper]
            discount_pct = promo_info["discount_percent"]
            discount_amount = int(base_price * discount_pct / 100)
            final_price = base_price - discount_amount
            return (
                f"💰 Học phí khóa [{course['course_id']}] {course['name']}:\n"
                f"- Giá gốc: {base_price:,} VNĐ\n"
                f"- Áp dụng mã [{code_upper}]: {promo_info['description']}\n"
                f"- Số tiền được giảm: -{discount_amount:,} VNĐ\n"
                f"- Tổng chi phí thanh toán cuối cùng: {final_price:,} VNĐ"
            )
        else:
            return (
                f"⚠️ Mã giảm giá '{promo_code}' không hợp lệ hoặc đã hết hạn.\n"
                f"💰 Học phí gốc khóa [{course['course_id']}] vẫn là: {base_price:,} VNĐ."
            )
    except Exception as e:
        return f"LỖI HỆ THỐNG khi tính học phí: {str(e)}"


# =============================================================================
# 📋 REGISTRY ĐĂNG KÝ TOOL (100% MATCH VỚI SPEC MD)
# =============================================================================
AVAILABLE_TOOLS = {
    "suggest_level": suggest_level,
    "search_courses": search_courses,
    "get_course_detail": get_course_detail,
    "check_schedule": check_schedule,
    "compare_courses": compare_courses,
    "calculate_price": calculate_price,
}
