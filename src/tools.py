
"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề: Trợ Lý Tư Vấn Khóa Học Tiếng Anh (IELTS & TOEIC)
File code được chuẩn hóa chính xác theo spec trong docs/role2_tools_spec.md
Dữ liệu mock được đọc trực tiếp từ config/mock_data.json.
"""

import json
import os

# =============================================================================
# 📂 NẠP DỮ LIỆU MOCK TỪ config/mock_data.json
# =============================================================================
_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "mock_data.json")

with open(_DATA_PATH, "r", encoding="utf-8") as _f:
    _MOCK_DATA = json.load(_f)

COURSES_DB = _MOCK_DATA["courses"]
ALIAS_MAP = _MOCK_DATA.get("alias_map", {})
PROMO_CODES = _MOCK_DATA.get("promo_codes", {})


def get_course_by_id(course_id: str):
    """Tra cứu khóa học theo mã, hỗ trợ cả các mã alias trong ALIAS_MAP."""
    cid = str(course_id).strip().upper()
    cid = ALIAS_MAP.get(cid, cid)
    return COURSES_DB.get(cid)


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
                suggested_course = "IELTS_BEGIN (IELTS Nền Tảng & Căn Bản)"
            elif score < 5.5:
                level = "Intermediate"
                suggested_course = "IELTS_INTER (IELTS Bứt Phá Mục Tiêu 5.5)"
            else:
                level = "Advanced"
                suggested_course = "IELTS_ADV (IELTS Chinh Phục Band Cao)"
        else:  # TOEIC
            if not (0 <= score <= 990):
                return f"LỖI: Điểm TOEIC '{score}' không hợp lệ (phải từ 0 đến 990)."
            if score < 350:
                level = "Beginner"
                suggested_course = "TOEIC_BEGIN (TOEIC Nền Tảng & Mất Gốc)"
            elif score < 650:
                level = "Intermediate"
                suggested_course = "TOEIC_INTER (TOEIC Mục Tiêu Ra Trường)"
            else:
                level = "Advanced"
                suggested_course = "TOEIC_ADV (TOEIC Đỉnh Cao Đạt Chuẩn)"

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
        course = get_course_by_id(course_id)
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
        course = get_course_by_id(course_id)
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
        if isinstance(course_ids_str, list):
            raw_ids = course_ids_str
        else:
            raw_ids = str(course_ids_str).split(",")

        cids = [c.strip().upper() for c in raw_ids if c.strip()]

        if len(cids) < 2:
            return "LỖI: Cần cung cấp ít nhất 2 mã khóa học hợp lệ để so sánh"

        courses = []
        for cid in cids:
            course = get_course_by_id(cid)
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
        course = get_course_by_id(course_id)
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
