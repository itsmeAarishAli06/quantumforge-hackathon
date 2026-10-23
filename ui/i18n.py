"""Localization dictionary and helper functions for English, Urdu, and Sindhi.

Keeps technical data (batch numbers, URLs, dates, official source titles) intact
while providing human-centered guidance in Pakistan's primary languages.
"""

from typing import Literal

LanguageCode = Literal["en", "ur", "sd"]

LANGUAGES: dict[str, str] = {
    "en": "English",
    "ur": "اردو (Urdu)",
    "sd": "سنڌي (Sindhi)",
}

RTL_LANGUAGES = {"ur", "sd"}

MESSAGES: dict[LanguageCode, dict[str, str]] = {
    "en": {
        # App identity & Topbar
        "app_title": "Dawa-Muhafiz",
        "app_tagline": "دوا محافظ — Medicine Safety & Rapid-Alert Assistant",
        "app_descriptor": "Medicine Alert Intelligence",
        "app_subtitle": "Screen visible packaging details against official DRAP alerts. We do not authenticate medicines or certify safety.",
        "badge_prototype": "PROTOTYPE · NOT AN OFFICIAL DRAP SERVICE",
        "badge_ai_ready": "AI Extraction Active",
        "badge_ai_demo": "Demo Mode Active",
        "nav_check_medicine": "Check Medicine",
        "nav_overview": "Overview",
        "nav_alert_info": "Alert Intelligence",
        "nav_about": "About Dawa-Muhafiz",
        
        # Overview / Hero
        "hero_headline": "A clearer way to check medicine alerts.",
        "hero_sub": "Review the details printed on your medicine packaging and compare them with the validated DRAP alerts available in our database.",
        "hero_cta_check": "Check a Medicine Now",
        "hero_cta_how": "Learn How It Works",
        "wf_card1_title": "01 — Upload Packaging",
        "wf_card1_desc": "Upload a clear photo of your carton, blister strip, or bottle. Images are processed in-memory and never stored.",
        "wf_card2_title": "02 — Review Details",
        "wf_card2_desc": "Inspect OCR-extracted packaging fields. Correct any blurred or misread text before checking.",
        "wf_card3_title": "03 — Check Official Alerts",
        "wf_card3_desc": "Compare reviewed batch and product details against validated DRAP rapid alerts and inspect official evidence.",
        "trust_heading": "Designed for Transparency & Healthcare Safety",
        "trust_desc": "Dawa-Muhafiz is an academic prototype built to empower healthcare workers, pharmacists, and citizens in Pakistan with accessible regulatory intelligence.",
        "trust_point1": "Strict Deterministic Matching: AI is only used to extract text; alert checking is strictly deterministic against verified records.",
        "trust_point2": "Traceable Regulatory Evidence: Every positive match provides the official DRAP document title, URL, publication date, and excerpt.",
        "trust_point3": "Honest Safety Boundaries: Absence of an alert match never implies a medicine is genuine, authentic, or approved.",
        "coverage_title": "Database Transparency",
        "coverage_desc": "Current version operates on human-reviewed DRAP rapid alert and recall fixtures. Real-time synchronization is scheduled for future phases.",

        # Alert Intelligence
        "alert_intel_title": "DRAP Alert Intelligence & Guidance",
        "alert_intel_sub": "Understanding official drug recalls, rapid alerts, and packaging identification in Pakistan.",
        "alert_intel_what_is": "What is a DRAP Rapid Alert?",
        "alert_intel_what_is_desc": (
            "The Drug Regulatory Authority of Pakistan (DRAP) issues Rapid Alerts when specific medicine batches "
            "fail laboratory quality standards, are found to be substandard, adulterated, falsified (spurious), or recalled by manufacturers."
        ),
        "alert_intel_batch_guide": "How to locate batch and lot numbers on packaging",
        "alert_intel_batch_desc": (
            "The batch or lot number (e.g., 'YT9D', 'B-1044') is typically stamped or embossed on the crimped edge of blister packs, "
            "the flap of cardboard cartons, or the side of liquid medicine bottles. It uniquely identifies the manufacturing run."
        ),
        "alert_intel_link_portal": "Visit Official DRAP Recall & Rapid Alert Portal",

        # About Project
        "about_proj_title": "About Dawa-Muhafiz (دوا محافظ)",
        "about_proj_sub": "An academic public safety prototype for Pakistani healthcare transparency.",
        "about_proj_mission": "Our Mission",
        "about_proj_mission_desc": (
            "Counterfeit and substandard medicines pose severe risks to patient health in Pakistan. "
            "Dawa-Muhafiz bridges the gap between complex regulatory PDF notices and everyday citizens, "
            "providing instant, localized screening tools without overpromising AI capabilities."
        ),
        "about_proj_ethics": "Ethical AI & Verification Invariants",
        "about_proj_ethics_desc": (
            "1. No AI-Generated Authenticity Verdicts: We never say a medicine is 'authentic' or 'fake' from an image.\n"
            "2. Deterministic Verification: Only exact or reviewed matches against DRAP data generate alerts.\n"
            "3. Privacy by Design: Zero permanent storage of user-uploaded images."
        ),

        # Step guide (Check Medicine)
        "step_1_title": "Upload packaging",
        "step_1_desc": "Clear JPG or PNG photo of carton, blister, or bottle.",
        "step_2_title": "Review details",
        "step_2_desc": "Verify extracted text and correct any OCR mistakes.",
        "step_3_title": "Screen alerts",
        "step_3_desc": "Compare against validated official DRAP records.",
        
        # Disclaimers
        "safety_disclaimer_title": "Important safety notice",
        "safety_disclaimer_text": (
            "Dawa-Muhafiz checks medicine details only against available official DRAP alerts in its database. "
            "No alert match does NOT guarantee that a medicine is genuine, authentic, or safe. "
            "Always consult a licensed pharmacist or physician for medical concerns."
        ),
        
        # Upload
        "upload_section_title": "1. Upload medicine packaging",
        "upload_label": "Choose or drop packaging photo",
        "upload_help": "Max 10 MB. JPG or PNG. The photo remains in this session and is never permanently stored.",
        "upload_btn_reset": "Start again",
        "upload_tips_title": "Photography tips for best results",
        "upload_tip_light": "Use good lighting and avoid reflections or harsh shadows.",
        "upload_tip_batch": "Ensure the batch number, brand, and expiry dates are sharp and in focus.",
        "upload_tip_angle": "Capture the packaging flat to avoid distorted or curved text.",
        "upload_success": "Image validated: {name} ({size} KB, {width}x{height} px)",
        
        # Extraction
        "extract_section_title": "2. Extract and review details",
        "extract_btn_live": "Extract with Gemini",
        "extract_btn_demo": "Use synthetic demo details",
        "extract_loading": "Reading packaging text with Gemini AI. Please wait...",
        "extract_success": "Text extracted successfully. Please review each field below against your package.",
        "extract_demo_notice": "SYNTHETIC DEMO DETAILS · These values were not read from your image.",
        "extract_gemini_privacy": "Image bytes were transmitted to Google Gemini for extraction. Do not upload personal information.",
        "extract_missing_key": "To enable AI extraction, add GEMINI_API_KEY to your .env file. Synthetic demo remains available.",
        
        # Fields
        "group_product": "Product information",
        "group_manufacturer": "Manufacturer & registration",
        "group_dates": "Dates & shelf life",
        "group_codes": "Barcodes & identifiers",
        "field_medicine_name": "Medicine name",
        "field_generic_name": "Generic / active ingredient",
        "field_strength": "Strength (e.g. 500 mg)",
        "field_dosage_form": "Dosage form (e.g. tablet, syrup)",
        "field_manufacturer_name": "Manufacturer name",
        "field_manufacturer_address": "Manufacturer address",
        "field_registration_number": "DRAP registration number",
        "field_batch_number": "Batch / lot number",
        "field_manufacturing_date": "Manufacturing date (YYYY-MM-DD)",
        "field_expiry_date": "Expiry date (YYYY-MM-DD)",
        "field_barcode_value": "Barcode value",
        "badge_extracted": "AI Extracted",
        "badge_edited": "User Corrected",
        "warn_batch_missing": "Batch or lot number is missing. DRAP alert screening requires a batch number to check specific recalls.",
        "warn_unreadable": "Unreadable or blurred fields: {fields}",
        
        # Screening / Results
        "screen_section_title": "3. Alert verification",
        "screen_preview_title": "Preview synthetic screening scenario (development preview)",
        "screen_preview_caption": "This selector simulates verification outcomes. Real DRAP database lookup is deferred.",
        "screen_btn_preview": "Preview screening result",
        "result_header": "Screening result",
        "result_demo_badge": "SYNTHETIC DEMO SCENARIO | No real alert lookup was performed",
        
        # Status specific
        "status_alert_match_title": "ALERT MATCH — Documented DRAP alert found",
        "status_alert_match_desc": "A matching record was found in the validated alert dataset. Review the official evidence below.",
        "status_alert_match_warning": "PRECAUTION: Do not consume or dispense this batch if it matches an official recall. Contact DRAP or a licensed pharmacist.",
        
        "status_verification_req_title": "VERIFICATION REQUIRED — Clarification needed",
        "status_verification_req_desc": "The extracted or entered details are incomplete, blurred, or ambiguous. Further checking is required.",
        "status_verification_req_action": "Check the physical package, correct missing fields above, or upload a sharper photo.",
        
        "status_no_match_title": "NO MATCH FOUND in the available database",
        "status_no_match_desc": "No matching alert was found in the available validated DRAP records.",
        "status_no_match_caveat": "IMPORTANT: This does NOT confirm that the medicine is genuine, authentic, approved, or safe. The database may not contain all current alerts.",
        
        "status_error_title": "ERROR — Check could not be completed",
        "status_error_desc": "The screening check encountered an error. Please try again or verify system connectivity.",
        
        # Evidence panel
        "evidence_title": "Official alert evidence & source details",
        "evidence_type": "Alert category",
        "evidence_product": "Product cited",
        "evidence_batch": "Affected batch",
        "evidence_excerpt": "Supporting excerpt from DRAP document",
        "evidence_source": "Official source reference",
        "evidence_link": "Open official DRAP source",
        "evidence_reasons": "Matching criteria",
        "evidence_dataset_count": "Records in checked dataset: {count}",
        "evidence_next_step": "Recommended next step: {step}",
        
        # Report
        "report_title": "Medicine Screening Summary",
        "report_btn": "Download screening summary (Text)",
        "report_timestamp": "Timestamp",
        "report_notice": "This document is an academic screening summary and does not constitute medical or regulatory advice.",
        
        # Footer
        "footer_about_title": "About Dawa-Muhafiz",
        "footer_about_text": "An academic prototype designed to empower Pakistani healthcare workers and citizens with transparent access to verified DRAP rapid alerts and product recalls.",
        "footer_privacy_text": "Privacy First: Uploaded packaging images are processed strictly in memory and are discarded when the session ends.",
        "footer_standards": "Adheres to WHO and DRAP safety reporting standards · Open for academic collaboration",
    },
    
    "ur": {
        # App identity & Topbar
        "app_title": "دوا محافظ",
        "app_tagline": "دوا محافظ — ادویات کی حفاظت اور الرٹ معاون",
        "app_descriptor": "ادویات الرٹ انٹیلیجنس",
        "app_subtitle": "پیکیجنگ کی تفصیلات کا DRAP کے سرکاری الرٹس کے ساتھ موازنہ کریں۔ یہ نظام ادویات کے اصلی ہونے کی تصدیق نہیں کرتا۔",
        "badge_prototype": "پروٹوٹائپ · غیر سرکاری DRAP سروس",
        "badge_ai_ready": "AI اخراج فعال ہے",
        "badge_ai_demo": "ڈیمو موڈ فعال ہے",
        "nav_check_medicine": "دوا چیک کریں",
        "nav_overview": "جائزہ",
        "nav_alert_info": "الرٹس رہنمائی",
        "nav_about": "دوا محافظ کے بارے میں",
        
        # Overview / Hero
        "hero_headline": "ادویات کے سرکاری الرٹس چیک کرنے کا محفوظ ترین طریقہ۔",
        "hero_sub": "اپنی دوا کی پیکیجنگ پر درج تفصیلات کا DRAP کے مصدقہ الرٹس کے ریکارڈ سے موازنہ کریں۔",
        "hero_cta_check": "دوا چیک کریں",
        "hero_cta_how": "طریقہ کار سمجھیں",
        "wf_card1_title": "۱ — پیکیجنگ تصویر اپلوڈ",
        "wf_card1_desc": "ڈبے، پتے یا بوتل کی تصویر اپلوڈ کریں۔ تصویر صرف میموری میں رہتی ہے اور محفوظ نہیں کی جاتی۔",
        "wf_card2_title": "۲ — تفصیلات کا جائزہ",
        "wf_card2_desc": "پڑھے گئے متن کی جانچ کریں اور الرٹ چیک کرنے سے پہلے کسی بھی غلطی کو درست کریں۔",
        "wf_card3_title": "۳ — سرکاری الرٹس کی جانچ",
        "wf_card3_desc": "تصدیق شدہ DRAP ریکارڈز سے بیچ نمبر کا موازنہ کریں اور سرکاری ثبوت ملاحظہ کریں۔",
        "trust_heading": "طبی حفاظت اور شفافیت کے اصول",
        "trust_desc": "دوا محافظ پاکستانی شہریوں اور فارماسسٹس کو ادویاتی انتباہات تک آسان رسائی فراہم کرتا ہے۔",
        "trust_point1": "طے شدہ تصدیقی طریقہ: AI صرف متن پڑھتا ہے، تصدیق خالصتاً سرکاری ریکارڈ سے ہوتی ہے۔",
        "trust_point2": "مصدقہ ثبوت: ہر الرٹ میچ کے ساتھ اصل سرکاری دستاویز، لنک اور تاریخ فراہم کی جاتی ہے۔",
        "trust_point3": "دیانت دارانہ حدود: الرٹ نہ ملنے کا مطلب دوا کے اصلی یا محفوظ ہونے کی ضمانت نہیں ہے۔",
        "coverage_title": "ڈیٹابیس شفافیت",
        "coverage_desc": "موجودہ ورژن انسانی جانچ شدہ DRAP الرٹس پر مشتمل ہے۔ مکمل لائیو سنکرونائزیشن آئندہ مراحل میں شامل کی جائے گی۔",

        # Alert Intelligence
        "alert_intel_title": "سرکاری DRAP الرٹس انٹیلیجنس",
        "alert_intel_sub": "پاکستان میں ادویات کی منسوخی، ریپڈ الرٹس اور بیچ نمبرز کی تفہیم۔",
        "alert_intel_what_is": "DRAP ریپڈ الرٹ کیا ہے؟",
        "alert_intel_what_is_desc": (
            "ڈرگ ریگولیٹری اتھارٹی آف پاکستان (DRAP) اس وقت ریپڈ الرٹ جاری کرتی ہے جب کوئی مخصوص دوا لیبارٹری ٹیسٹ میں غیر معیاری ثابت ہو یا جعلی پائی جائے۔"
        ),
        "alert_intel_batch_guide": "پیکیجنگ پر بیچ نمبر کیسے تلاش کریں؟",
        "alert_intel_batch_desc": (
            "بیچ یا لاٹ نمبر عام طور پر پتے کے کنارے پر یا ڈبے کے اوپر ابھرا ہوا ہوتا ہے (مثلاً 'YT9D')۔ یہ دوا کی مخصوص تیاری کی نشاندہی کرتا ہے۔"
        ),
        "alert_intel_link_portal": "سرکاری DRAP پورٹل پر جائیں",

        # About Project
        "about_proj_title": "دوا محافظ کے بارے میں",
        "about_proj_sub": "پاکستانی عوام کی صحت کے تحفظ کے لیے تیار کردہ تعلیمی پروٹوٹائپ۔",
        "about_proj_mission": "ہمارا مقصد",
        "about_proj_mission_desc": (
            "غیر معیاری اور جعلی ادویات مریضوں کے لیے خطرناک ثابت ہو سکتی ہیں۔ دوا محافظ ریگولیٹری دستاویزات کو عام فہم بناتا ہے۔"
        ),
        "about_proj_ethics": "اخلاقی و تکنیکی حدود",
        "about_proj_ethics_desc": (
            "۱. AI کبھی دوا کے اصلی ہونے کا فیصلہ نہیں کرتا۔\n"
            "۲. الرٹ کی جانچ صرف مصدقہ ریکارڈز سے ہوتی ہے۔\n"
            "۳. رازداری کی مکمل ضمانت: تصاویر کو محفوظ نہیں کیا جاتا۔"
        ),

        # Step guide
        "step_1_title": "پیکیجنگ تصویر",
        "step_1_desc": "ڈبے، پتے یا بوتل کی واضح تصویر اپلوڈ کریں۔",
        "step_2_title": "تفصیلات کی جانچ",
        "step_2_desc": "پڑھے گئے متن کی تصدیق کریں اور غلطیاں درست کریں۔",
        "step_3_title": "الرٹس کی جانچ",
        "step_3_desc": "سرکاری DRAP الرٹس کے ریکارڈ سے موازنہ کریں۔",
        
        # Disclaimers
        "safety_disclaimer_title": "اہم طبی و حفاظتی انتباہ",
        "safety_disclaimer_text": (
            "دوا محافظ ادویات کی تفصیلات صرف اپنے پاس موجود DRAP کے سرکاری الرٹس سے چیک کرتا ہے۔ "
            "کوئی الرٹ نہ ملنے کا مطلب ہرگز یہ نہیں کہ دوا اصلی، منظور شدہ یا محفوظ ہے۔ "
            "کسی بھی تشویش کی صورت میں ہمیشہ مستند فارماسسٹ یا ڈاکٹر سے رجوع کریں۔"
        ),
        
        # Upload
        "upload_section_title": "۱. دوا کی پیکیجنگ اپلوڈ کریں",
        "upload_label": "تصویر منتخب کریں یا یہاں ڈراپ کریں",
        "upload_help": "زیادہ سے زیادہ 10 MB۔ صرف JPG یا PNG۔ تصویر صرف موجودہ سیشن میں رہتی ہے اور محفوظ نہیں کی جاتی۔",
        "upload_btn_reset": "دوبارہ شروع کریں",
        "upload_tips_title": "بہترین نتائج کے لیے تصویر کے رہنما اصول",
        "upload_tip_light": "اچھی روشنی کا استعمال کریں اور چمک یا سائے سے بچیں۔",
        "upload_tip_batch": "بیچ نمبر، نام اور ایکسپائری تاریخ بالکل واضح ہونی چاہیے۔",
        "upload_tip_angle": "تصویر کو بالکل سیدھا کھینچیں تاکہ متن ٹیڑھا نہ ہو۔",
        "upload_success": "تصویر کی تصدیق ہو گئی: {name} ({size} KB)",
        
        # Extraction
        "extract_section_title": "۲. تفصیلات کا اخراج اور جائزہ",
        "extract_btn_live": "Gemini AI سے متن پڑھیں",
        "extract_btn_demo": "مصنوعی ڈیمو ڈیٹا استعمال کریں",
        "extract_loading": "Gemini AI پیکیجنگ سے متن پڑھ رہا ہے، براہ کرم انتظار کریں...",
        "extract_success": "متن کامیابی سے حاصل کر لیا گیا۔ براہ کرم دوا کے ڈبے سے موازنہ کر کے تصدیق کریں۔",
        "extract_demo_notice": "مصنوعی ڈیمو تفصیلات · یہ معلومات آپ کی تصویر سے نہیں پڑھی گئی ہیں۔",
        "extract_gemini_privacy": "تصویر Gemini سروس کو بھیجی گئی ہے۔ ذاتی معلومات والی تصاویر اپلوڈ نہ کریں۔",
        "extract_missing_key": "AI سے متن پڑھنے کے لیے .env میں GEMINI_API_KEY شامل کریں۔ ڈیمو موڈ فعال ہے۔",
        
        # Fields
        "group_product": "دوا کی معلومات",
        "group_manufacturer": "سازندہ اور رجسٹریشن",
        "group_dates": "تاریخیں اور میعاد",
        "group_codes": "بارکوڈ اور شناختی نمبر",
        "field_medicine_name": "دوا کا نام",
        "field_generic_name": "فارمولا / متحرک جزو",
        "field_strength": "طاقت (مثلاً 500 mg)",
        "field_dosage_form": "شکل (مثلاً گولی، شربت)",
        "field_manufacturer_name": "کمپنی / مینوفیکچرر کا نام",
        "field_manufacturer_address": "کمپنی کا پتہ",
        "field_registration_number": "DRAP رجسٹریشن نمبر",
        "field_batch_number": "بیچ / لاٹ نمبر",
        "field_manufacturing_date": "تاریخ پیدائش (YYYY-MM-DD)",
        "field_expiry_date": "تاریخ تنسیخ (YYYY-MM-DD)",
        "field_barcode_value": "بارکوڈ ویلیو",
        "badge_extracted": "AI اخراج",
        "badge_edited": "صارف کی تصحیح",
        "warn_batch_missing": "بیچ یا لاٹ نمبر غائب ہے۔ مخصوص الرٹ چیک کرنے کے لیے بیچ نمبر ضروری ہے۔",
        "warn_unreadable": "ناقابلِ قرات یا دھندلے فیلڈز: {fields}",
        
        # Screening / Results
        "screen_section_title": "۳. الرٹ جانچ",
        "screen_preview_title": "مصنوعی اسکریننگ منظر نامہ پیش نظارہ (ترقیاتی)",
        "screen_preview_caption": "یہ سلیکٹر ممکنہ نتائج دکھانے کے لیے ہے۔ حقیقی ڈیٹابیس کا مکمل سرچ مرحلہ وار شامل کیا جا رہا ہے۔",
        "screen_btn_preview": "نتیجے کا پیش نظارہ دیکھیں",
        "result_header": "جانچ کا نتیجہ",
        "result_demo_badge": "مصنوعی ڈیمو منظر نامہ | کوئی حقیقی الرٹ چیک نہیں کیا گیا",
        
        # Status specific
        "status_alert_match_title": "الرٹ میچ — سرکاری DRAP انتباہ موجود ہے",
        "status_alert_match_desc": "تصدیق شدہ الرٹس میں مماثل ریکارڈ پایا گیا ہے۔ نیچے سرکاری ثبوت ملاحظہ کریں۔",
        "status_alert_match_warning": "احتیاط: اگر یہ بیچ سرکاری واپسی کے الرٹ سے ملتا ہے تو اسے ہرگز استعمال نہ کریں۔ فوری طور پر فارماسسٹ یا DRAP سے رابطہ کریں۔",
        
        "status_verification_req_title": "مزید تصدیق درکار ہے",
        "status_verification_req_desc": "درج کردہ تفصیلات نامکمل، دھندلی یا غیر واضح ہیں۔ مزید تصدیق ضروری ہے۔",
        "status_verification_req_action": "براہ کرم ڈبے سے معلومات چیک کریں، نامکمل فیلڈز درج کریں، یا زیادہ واضح تصویر اپلوڈ کریں۔",
        
        "status_no_match_title": "دستیاب ڈیٹابیس میں کوئی الرٹ نہیں ملا",
        "status_no_match_desc": "موجودہ تصدیق شدہ DRAP ریکارڈز میں اس بیچ کے خلاف کوئی انتباہ درج نہیں ہے۔",
        "status_no_match_caveat": "اہم: اس کا مطلب ہرگز یہ نہیں کہ دوا اصلی، منظور شدہ یا محفوظ ہے۔ ہو سکتا ہے کہ ڈیٹا بیس میں تمام الرٹس شامل نہ ہوں۔",
        
        "status_error_title": "خرابی — جانچ مکمل نہیں ہو سکی",
        "status_error_desc": "تکنیکی خرابی کے باعث چیک مکمل نہیں ہو سکا۔ براہ کرم دوبارہ کوشش کریں۔",
        
        # Evidence panel
        "evidence_title": "سرکاری الرٹ کے ثبوت اور تفصیلات",
        "evidence_type": "الرٹ کی قسم",
        "evidence_product": "متاثرہ پروڈکٹ",
        "evidence_batch": "متاثرہ بیچ",
        "evidence_excerpt": "DRAP دستاویز سے اقتباس",
        "evidence_source": "سرکاری ماخذ عنوان",
        "evidence_link": "اصل DRAP ماخذ دستاویز کھولیں",
        "evidence_reasons": "مماثلت کی وجوہات",
        "evidence_dataset_count": "چیک کردہ ریکارڈز کی تعداد: {count}",
        "evidence_next_step": "تجویز کردہ اگلا قدم: {step}",
        
        # Report
        "report_title": "دوا کی اسکریننگ خلاصہ",
        "report_btn": "اسکریننگ خلاصہ ڈاؤن لوڈ کریں (متن)",
        "report_timestamp": "وقت اور تاریخ",
        "report_notice": "یہ دستاویز ایک تعلیمی اسکریننگ خلاصہ ہے اور یہ طبی یا قانونی سند نہیں ہے۔",
        
        # Footer
        "footer_about_title": "دوا محافظ کے بارے میں",
        "footer_about_text": "ایک تعلیمی پروٹوٹائپ جو پاکستانی شہریوں اور ہیلتھ کیئر ورکرز کو DRAP کے مصدقہ الرٹس تک شفاف رسائی فراہم کرتا ہے۔",
        "footer_privacy_text": "رازداری کی ضمانت: تصاویر صرف میموری میں پروسیس ہوتی ہیں اور سیشن ختم ہونے پر مٹا دی جاتی ہیں۔",
        "footer_standards": "WHO اور DRAP کے حفاظتی معیارات کے مطابق مرتب کردہ",
    },
    
    "sd": {
        # App identity & Topbar
        "app_title": "دوا محافظ",
        "app_tagline": "دوا محافظ — دوائن جي حفاظت ۽ الرٽ مددگار",
        "app_descriptor": "دوائن جو الرٽ نظام",
        "app_subtitle": "پيڪيجنگ جي تفصيلن جو DRAP جي سرڪاري الرٽس سان موازنو ڪريو. هي سسٽم دوا جي اصلي هجڻ جي پڪ نٿو ڪري.",
        "badge_prototype": "پروٽوٽائپ · غير سرڪاري DRAP سهولت",
        "badge_ai_ready": "AI ذريعي لکت پڙهڻ فعال آهي",
        "badge_ai_demo": "ڊيمو موڊ فعال آهي",
        "nav_check_medicine": "دوا چيڪ ڪريو",
        "nav_overview": "خلاصو",
        "nav_alert_info": "الرٽ ڄاڻ",
        "nav_about": "دوا محافظ بابت",
        
        # Overview / Hero
        "hero_headline": "دوائن جا سرڪاري الرٽ چيڪ ڪرڻ جو محفوظ رستو.",
        "hero_sub": "پنهنجي دوا جي پيڪنگ تي لکيل تفصيلن جي DRAP جي تصديق ٿيل الرٽس سان ڀيٽ ڪريو.",
        "hero_cta_check": "دوا چيڪ ڪريو",
        "hero_cta_how": "طريقو سمجھو",
        "wf_card1_title": "۱ — پيڪنگ جي تصوير اپلوڊ",
        "wf_card1_desc": "دٻي يا پتي جي چٽي تصوير اپلوڊ ڪريو. تصويرون رڳو ميموري ۾ رهنديون آهن.",
        "wf_card2_title": "۲ — تفصيلن جي چڪاس",
        "wf_card2_desc": "پڙهيل لکت جو جائزو وٺو ۽ الرٽ چيڪ ڪرڻ کان اڳ غلطيون درست ڪريو.",
        "wf_card3_title": "۳ — سرڪاري الرٽس جي ڀيٽ",
        "wf_card3_desc": "تصديق ٿيل DRAP رڪارڊز مان بيچ نمبر چيڪ ڪريو ۽ سرڪاري ثبوت ڏسو.",
        "trust_heading": "شفافيت ۽ طبي حفاظت جا اصول",
        "trust_desc": "دوا محافظ پاڪستاني شهرين ۽ صحت ڪارڪنن کي DRAP الرٽس تائين سڌي رسائي ڏئي ٿو.",
        "trust_point1": "پڪو طريقو: AI رڳو لکت پڙهي ٿو، چڪاس سرڪاري رڪارڊ ذريعي ٿئي ٿي.",
        "trust_point2": "سرڪاري ثبوت: هر الرٽ سان سرڪاري لنڪ، تاريخ ۽ اقتباس ڏنو وڃي ٿو.",
        "trust_point3": "حفاظتي حدون: الرٽ نه ملڻ جو مطلب دوا جي اصلي هجڻ جي پڪ ناهي.",
        "coverage_title": "ڊيٽابيس شفافيت",
        "coverage_desc": "موجوده نسخو نظرثاني ٿيل DRAP الرٽس تي ٻڌل آهي. مڪمل لائیو سهولت جلد شامل ٿيندي.",

        # Alert Intelligence
        "alert_intel_title": "سرڪاري DRAP الرٽس رهنمائي",
        "alert_intel_sub": "پاڪستان ۾ دوائن جي واپسي ۽ بيچ نمبرن جي سمجھاڻي.",
        "alert_intel_what_is": "DRAP ريپڊ الرٽ ڇا آهي؟",
        "alert_intel_what_is_desc": (
            "ڊرگ ريگيوليٽري اٿارٽي آف پاڪستان (DRAP) تڏهن الرٽ جاري ڪري ٿي جڏهن ڪا دوا غير معياري يا جعلي هجي."
        ),
        "alert_intel_batch_guide": "پيڪنگ مان بيچ نمبر ڪيئن ڳولجي؟",
        "alert_intel_batch_desc": (
            "بيچ نمبر گهڻو ڪري پتي جي ڪنڊ يا دٻي تي لکيل هوندو آهي (مثال: 'YT9D')."
        ),
        "alert_intel_link_portal": "سرڪاري DRAP پورٽل ڏسو",

        # About Project
        "about_proj_title": "دوا محافظ بابت",
        "about_proj_sub": "عوامي صحت جي بهتري لاءِ هڪ تعليمي پليٽ فارم.",
        "about_proj_mission": "اسان جو مقصد",
        "about_proj_mission_desc": (
            "جعلي دوائن کان عوام کي خبردار رکڻ ۽ ريگيوليٽري معلومات کي عام ڪرڻ اسان جو مقصد آهي."
        ),
        "about_proj_ethics": "اخلاقي ۽ فني اصول",
        "about_proj_ethics_desc": (
            "۱. AI دوا جي اصلي هجڻ جو فيصلو نٿو ڪري.\n"
            "۲. چڪاس صرف سرڪاري رڪارڊ مان ٿئي ٿي.\n"
            "۳. رازداري: تصويرون محفوظ نه ٿيون ڪيون وڃن."
        ),

        # Step guide
        "step_1_title": "پيڪنگ جي تصوير",
        "step_1_desc": "پتي، دٻي يا بوتل جي چٽي تصوير اپلوڊ ڪريو.",
        "step_2_title": "تفصيلن جي چڪاس",
        "step_2_desc": "پڙهيل لکت جي تصديق ڪريو ۽ غلطيون درست ڪريو.",
        "step_3_title": "الرٽس جي ڀيٽ",
        "step_3_desc": "سرڪاري DRAP الرٽس جي رڪارڊ سان ڀيٽ ڪريو.",
        
        # Disclaimers
        "safety_disclaimer_title": "اهم طبي ۽ حفاظتي هدايت",
        "safety_disclaimer_text": (
            "دوا محافظ صرف پنهنجي وٽ موجود DRAP الرٽس مان دوا چيڪ ڪري ٿو. "
            "ڪو الرٽ نه ملڻ جو مطلب بلڪل اهو ناهي ته دوا اصلي يا محفوظ آهي. "
            "طبي معاملي لاءِ هميشه مستند فارماسسٽ يا ڊاڪٽر سان رابطو ڪريو."
        ),
        
        # Upload
        "upload_section_title": "۱. دوا جي پيڪنگ جي تصوير اپلوڊ ڪريو",
        "upload_label": "تصوير چونڊيو يا هتي ڇڏيو",
        "upload_help": "وڌ ۾ وڌ 10 MB. صرف JPG يا PNG. تصوير صرف هن سيشن ۾ رهي ٿي.",
        "upload_btn_reset": "ٻيهر شروع ڪريو",
        "upload_tips_title": "سٺي تصوير لاءِ هدايتون",
        "upload_tip_light": "سٺي روشني استعمال ڪريو ۽ پاڇي کان بچو.",
        "upload_tip_batch": "بيچ نمبر، نالو ۽ ميعاد جي تاريخ واضح هجڻ گهرجي.",
        "upload_tip_angle": "تصوير سڌي وٺو ته جيئن اکر چٽا نظر اچن.",
        "upload_success": "تصوير تصديق ٿي وئي: {name} ({size} KB)",
        
        # Extraction
        "extract_section_title": "۲. تفصيلن جو اڀياس ۽ جائزو",
        "extract_btn_live": "Gemini AI سان پڙهو",
        "extract_btn_demo": "مصنوعي ڊيمو تفصيل استعمال ڪريو",
        "extract_loading": "Gemini AI پيڪنگ مان لکت پڙهي رهيو آهي، مهرباني ڪري انتظار ڪريو...",
        "extract_success": "تفصيل ڪاميابيءَ سان مليا. مهرباني ڪري دوا جي دٻي سان ڀيٽ ڪريو.",
        "extract_demo_notice": "مصنوعي ڊيمو تفصيل · هي معلومات اوهان جي تصوير مان ناهي پڙهي وئي.",
        "extract_gemini_privacy": "تصوير Gemini سروس ڏانهن موڪلي وئي آهي. ذاتي تصويرون اپلوڊ نه ڪريو.",
        "extract_missing_key": "AI استعمال ڪرڻ لاءِ .env ۾ GEMINI_API_KEY لکو. ڊيمو موڊ موجود آهي.",
        
        # Fields
        "group_product": "دوا بابت معلومات",
        "group_manufacturer": "ڪمپني ۽ رجسٽريشن",
        "group_dates": "تاريخون ۽ ميعاد",
        "group_codes": "بارڪوڊ ۽ سڃاڻپ",
        "field_medicine_name": "دوا جو نالو",
        "field_generic_name": "فارمولا / جُز",
        "field_strength": "طاقت (مثال: 500 mg)",
        "field_dosage_form": "صورت (مثال: گوري، شربت)",
        "field_manufacturer_name": "ڪمپني جو نالو",
        "field_manufacturer_address": "ڪمپني جي پتي",
        "field_registration_number": "DRAP رجسٽريشن نمبر",
        "field_batch_number": "بيچ / لاٽ نمبر",
        "field_manufacturing_date": "ٺهڻ جي تاريخ (YYYY-MM-DD)",
        "field_expiry_date": "ميعاد ختم ٿيڻ جي تاريخ (YYYY-MM-DD)",
        "field_barcode_value": "بارڪوڊ ويلو",
        "badge_extracted": "AI پڙهيل",
        "badge_edited": "درست ڪيل",
        "warn_batch_missing": "بيچ نمبر ناهي مليو. مخصوص الرٽ جانچڻ لاءِ بيچ نمبر ضروري آهي.",
        "warn_unreadable": "نه پڙهجندڙ خانا: {fields}",
        
        # Screening / Results
        "screen_section_title": "۳. الرٽ جي چڪاس",
        "screen_preview_title": "مصنوعي اسڪريننگ منظر نامي جو ڏيک (ترقياتي)",
        "screen_preview_caption": "هي چونڊ امڪاني نتيجا ڏيکارڻ لاءِ آهي. اصل رڪارڊ جي چڪاس جلد شامل ڪئي ويندي.",
        "screen_btn_preview": "نتيجن جو پيش نظارو ڏسو",
        "result_header": "اسڪريننگ نتيجو",
        "result_demo_badge": "مصنوعي ڊيمو منظر نامو | ڪو اصل الرٽ ناهي چيڪ ڪيو ويو",
        
        # Status specific
        "status_alert_match_title": "الرٽ ميچ — DRAP سرڪاري الرٽ ملي ويو",
        "status_alert_match_desc": "تصديق ٿيل الرٽس ۾ هڪجهڙو رڪارڊ مليو آهي. هيٺ سرڪاري ثبوت ڏسو.",
        "status_alert_match_warning": "احتياط: جيڪڏهن هي بيچ سرڪاري الرٽ سان ملي ٿو ته ان کي بلڪل استعمال نه ڪريو. فارماسسٽ سان رابطو ڪريو.",
        
        "status_verification_req_title": "وڌيڪ تصديق گهربل آهي",
        "status_verification_req_desc": "ڏنل تفصيل اڻپورا يا اڻ چٽا آهن. وڌيڪ تصديق ضروري آهي.",
        "status_verification_req_action": "مهرباني ڪري دٻي مان معلومات چيڪ ڪريو يا وڌيڪ چٽي تصوير اپلوڊ ڪريو.",
        
        "status_no_match_title": "موجود ڊيٽابيس ۾ ڪو الرٽ ناهي مليو",
        "status_no_match_desc": "موجود تصديق ٿيل DRAP رڪارڊ ۾ هن بيچ خلاف ڪو الرٽ ناهي.",
        "status_no_match_caveat": "اهم: هن جو مطلب بلڪل اهو ناهي ته دوا اصلي يا محفوظ آهي. ممڪن آهي ته سڀ الرٽ ڊيٽابيس ۾ نه هجن.",
        
        "status_error_title": "غلطي — چڪاس مڪمل نه ٿي سگهي",
        "status_error_desc": "ٽيڪنيڪل خرابي سبب چڪاس مڪمل نه ٿي. مهرباني ڪري ٻيهر ڪوشش ڪريو.",
        
        # Evidence panel
        "evidence_title": "سرڪاري الرٽ ثبوت ۽ تفصيل",
        "evidence_type": "الرٽ جو قسم",
        "evidence_product": "متاثر پراڊڪٽ",
        "evidence_batch": "متاثر بيچ",
        "evidence_excerpt": "DRAP دستاويز مان اقتباس",
        "evidence_source": "سرڪاري ذريعو",
        "evidence_link": "اصل DRAP دستاويز کوليو",
        "evidence_reasons": "ملندڙ سبب",
        "evidence_dataset_count": "چيڪ ڪيل رڪارڊن جو تعداد: {count}",
        "evidence_next_step": "تجويز ڪيل ايندڙ قدم: {step}",
        
        # Report
        "report_title": "دوا جي اسڪريننگ جو خلاصو",
        "report_btn": "خلاصو ڊائون لوڊ ڪريو (متن)",
        "report_timestamp": "وقت ۽ تاريخ",
        "report_notice": "هي دستاويز هڪ تعليمي اسڪريننگ خلاصو آهي ۽ هي ڪو طبي يا قانوني سرٽيفڪيٽ ناهي.",
        
        # Footer
        "footer_about_title": "دوا محافظ بابت",
        "footer_about_text": "هڪ تعليمي پروٽوٽائپ جيڪو پاڪستاني شهرين ۽ صحت جي ڪارڪنن کي DRAP الرٽس تائين سڌي رسائي ڏئي ٿو.",
        "footer_privacy_text": "رازداري جي پڪ: تصويرون رڳو ميموري ۾ پروسيس ٿين ٿيون ۽ سيشن ختم ٿيڻ تي مٽجي وڃن ٿيون.",
        "footer_standards": "WHO ۽ DRAP جي حفاظتي اصولن مطابق ٺهيل",
    },
}


def t(key: str, lang: str = "en", **kwargs: object) -> str:
    """Retrieve localized string with graceful fallback to English."""
    selected_lang: LanguageCode = lang if lang in MESSAGES else "en"
    text = MESSAGES[selected_lang].get(key) or MESSAGES["en"].get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text


def is_rtl(lang: str) -> bool:
    """Check if the selected language reads Right-to-Left."""
    return lang in RTL_LANGUAGES
