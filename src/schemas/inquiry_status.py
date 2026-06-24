from enum import Enum


class InquiryStatus(str, Enum):
    NEW = "New"
    COLLECTING_INFORMATION = "Collecting Information"
    CONFIRMED = "Confirmed"
    ASSESSMENT_COMPLETED = "Assessment Completed"
    REPORT_GENERATED = "Report Generated"
    CLOSED = "Closed"