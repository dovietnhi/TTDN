from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
    
from typing import Any, Text, Dict, List

class ActionSuggestTopics(Action):
    def name(self) -> Text:
        return "action_suggest_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_intent = tracker.latest_message.get("intent", {}).get("name")
        intent_ranking = tracker.latest_message.get("intent_ranking", []) or []

        # Lấy top 3 intent khác intent hiện tại
        suggestions = [i['name'] for i in intent_ranking if i.get('name') and i['name'] != last_intent][:3]

        if suggestions:
            buttons = []
            for sug in suggestions:
                title = sug.replace("_", " ").capitalize()
                payload = f"/{sug}"
                buttons.append({"title": title, "payload": payload})
            dispatcher.utter_message(text="Bạn có muốn hỏi thêm về:", buttons=buttons)
        else:
            dispatcher.utter_message(text="Mình chưa có gợi ý lúc này.")
        return []

class ActionContactInfo(Action):
    def name(self):
        return "action_contact_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
        contact_type = tracker.get_slot("contact_type")
        message = ""

        if contact_type:
            ct = contact_type.lower()

            if any(word in ct for word in ["hotline", "số điện thoại", "tổng đài"]):
                message = "📞 Hotline của công ty là 024-6686-4555 nhé."
            elif any(word in ct for word in ["email", "mail"]):
                message = "📧 Email hỗ trợ khách hàng là contact@vanvietsoft.com."
            elif any(word in ct for word in ["địa chỉ", "văn phòng", "trụ sở"]):
                message = "🏢 Địa chỉ: Tòa nhà Licogi 13, 164 Khuất Duy Tiến, Hà Nội."
            elif any(word in ct for word in ["zalo"]):
                message = "💬 Zalo chăm sóc khách hàng: 024-6686-4555."
            elif any(word in ct for word in ["website", "trang web"]):
                message = "🌐 Website chính thức: https://vanvietsoft.com."
            elif any(word in ct for word in ["facebook", "fanpage", "messenger"]):
                message = "📘 Fanpage: https://facebook.com/vanvietsoft"
            elif any(word in ct for word in ["telegram"]):
                message = "Hiện tại công ty chưa hỗ trợ qua Telegram."
            else:
                message = (
                    "Bạn có thể liên hệ qua hotline 024-6686-4555 hoặc "
                    "email contact@vanvietsoft.com nhé."
                )
        else:
            message = (
                "Bạn có thể liên hệ với V2S qua hotline 024-6686-4555 "
                "hoặc email contact@vanvietsoft.com."
            )

        dispatcher.utter_message(text=message)
        return [SlotSet("contact_type", None)]
class ActionCompanyInfo(Action):
    def name(self):
        return "action_company_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
        org = tracker.get_slot("organization") or "Công ty V2S"
        info = tracker.get_slot("info_type")

        if info in ["lĩnh vực", "ngành nghề"]:
            dispatcher.utter_message(f"{org} hoạt động trong lĩnh vực phát triển phần mềm và giải pháp quản lý doanh nghiệp, bao gồm ERP, CRM và chuyển đổi số.")
        elif info in ["sản phẩm", "giải pháp", "dịch vụ"]:
            dispatcher.utter_message(f"{org} cung cấp các sản phẩm phần mềm như ERP, CRM, hóa đơn điện tử, quản lý nhân sự, quản lý giáo dục, và phát triển phần mềm theo yêu cầu.")
        elif info in ["định hướng", "mục tiêu", "sứ mệnh"]:
            dispatcher.utter_message(f"{org} hướng đến việc trở thành nhà cung cấp giải pháp chuyển đổi số hàng đầu Việt Nam, giúp doanh nghiệp tối ưu vận hành và phát triển bền vững.")
        else:
            dispatcher.utter_message(f"{org} là công ty công nghệ Việt Nam chuyên cung cấp các giải pháp phần mềm ERP, CRM và dịch vụ chuyển đổi số cho doanh nghiệp.")
        return [
            SlotSet("organization", None),
            SlotSet("info_type", None)
        ]
class ActionTellCompanyLocation(Action):
    def name(self):
        return "action_tell_company_location"

    def run(self, dispatcher, tracker, domain):
        address = tracker.get_slot("company_address")

        if address and "hcm" in address.lower():
            dispatcher.utter_message(text="Hiện tại bên mình chưa có chi nhánh ở TP.HCM nhé.")
        else:
            dispatcher.utter_message(text="Trụ sở chính của V2S nằm tại Tầng 8, Tòa nhà XYZ, Cầu Giấy, Hà Nội.")
        return [SlotSet("company_address", None)]
class ActionWorkingHours(Action):
    def name(self):
        return "action_working_hours"

    def run(self, dispatcher, tracker, domain):
        period = tracker.get_slot("work_time_period")

        if period:
            if "cuối tuần" in period or "thứ 7" in period or "chủ nhật" in period:
                dispatcher.utter_message(text="Công ty làm việc từ thứ 2 đến thứ 6, nghỉ cuối tuần bạn nhé.")
            elif "ngày lễ" in period:
                dispatcher.utter_message(text="Vào các ngày lễ, công ty sẽ nghỉ theo quy định của Nhà nước.")
            elif "buổi tối" in period:
                dispatcher.utter_message(text="Hiện tại công ty chỉ làm việc trong giờ hành chính, không làm buổi tối.")
            elif "trưa" in period:
                dispatcher.utter_message(text="Công ty nghỉ trưa từ 12h đến 13h30.")
            elif "24/7" in period:
                dispatcher.utter_message(text="Bộ phận kỹ thuật có thể hỗ trợ 24/7, nhưng văn phòng hành chính chỉ làm giờ hành chính.")
            else:
                dispatcher.utter_message(text="Công ty làm việc giờ hành chính, từ 8h00 đến 17h00, thứ 2 đến thứ 6.")
        else:
            dispatcher.utter_message(text="Công ty V2S làm việc từ 8h00 đến 17h00, từ thứ 2 đến thứ 6 hàng tuần.")
        return [SlotSet("work_time_period", None)]
class ActionProductInfo(Action):
    def name(self):
        return "action_product_info"

    def run(self, dispatcher, tracker, domain):
        product = tracker.get_slot("product")

        if product:
            if "ERP" in product.upper():
                dispatcher.utter_message(text="Phần mềm ERP của V2S giúp quản lý toàn bộ hoạt động doanh nghiệp, từ kế toán, nhân sự đến bán hàng và kho vận.")
            elif "CRM" in product.upper():
                dispatcher.utter_message(text="Giải pháp CRM của V2S giúp doanh nghiệp quản lý khách hàng, chăm sóc và tăng hiệu quả bán hàng.")
            elif "hóa đơn điện tử" in product.lower():
                dispatcher.utter_message(text="Phần mềm hóa đơn điện tử của V2S là công cụ giúp doanh nghiệp tạo, gửi và quản lý hóa đơn điện tử theo quy định của Tổng cục Thuế, đồng thời dễ dàng tích hợp với các hệ thống khác.")
            elif "nhân sự" in product.lower():
                dispatcher.utter_message(text="Phần mềm quản lý nhân sự hỗ trợ chấm công, tính lương và quản lý hồ sơ nhân viên hiệu quả.")
            elif "giáo dục" in product.lower():
                dispatcher.utter_message(text="Giải pháp quản lý giáo dục của V2S giúp trường học tự động hóa quy trình quản lý học sinh, giáo viên và điểm số.")
            elif "bán hàng" in product.lower():
                dispatcher.utter_message(text="Phần mềm quản lý bán hàng hỗ trợ theo dõi đơn hàng, khách hàng và doanh thu theo thời gian thực.")
            elif "kho" in product.lower():
                dispatcher.utter_message(text="Phần mềm quản lý kho giúp kiểm soát xuất nhập tồn và định mức vật tư chính xác.")
            elif "tùy chỉnh" in product.lower() or "theo yêu cầu" in product.lower():
                dispatcher.utter_message(text="V2S có đội ngũ chuyên phát triển phần mềm theo yêu cầu riêng, phù hợp đặc thù từng doanh nghiệp.")
            else:
                dispatcher.utter_message(text=f"Hiện tại V2S có nhiều sản phẩm liên quan đến {product}, bạn có thể cho biết rõ hơn để mình tư vấn chi tiết?")
        else:
            dispatcher.utter_message(text="V2S cung cấp các giải pháp phần mềm như ERP, CRM, hóa đơn điện tử, nhân sự, giáo dục và nhiều sản phẩm khác.")
        return [SlotSet("product", None)]
class ActionProvidePricing(Action):
    def name(self):
        return "action_provide_pricing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        product = tracker.get_slot("product")

        if product:
            dispatcher.utter_message(
                text=f"Giá phần mềm {product} phụ thuộc vào quy mô và tính năng bạn cần. "
                    f"Bạn có muốn mình gửi báo giá chi tiết qua email không?"
            )
        else:
            dispatcher.utter_message(
                text="Giá phần mềm phụ thuộc vào từng sản phẩm. "
                    "Bạn muốn hỏi giá phần mềm nào ạ?"
            )

        return [SlotSet("email_context", "pricing")]


class ActionProvideDemo(Action):
    def name(self):
        return "action_provide_demo"

    def run(self, dispatcher, tracker, domain):
        product = tracker.get_slot("product")

        if product:
            dispatcher.utter_message(
                text=f"Công ty hiện có bản demo cho phần mềm {product}. "
                     "Bạn có muốn mình gửi link demo qua email không?"
            )
        else:
            dispatcher.utter_message(
                text="Bên mình có hỗ trợ demo cho nhiều phần mềm khác nhau. "
                     "Bạn có muốn mình gửi link demo và tài liệu hướng dẫn qua email không?"
            )

        # set slot email_context = demo để rule chọn đúng action khi người dùng affirm
        return [SlotSet("product", None), SlotSet("email_context", "demo")]
class ActionProvideDemo(Action):
    def name(self):
        return "action_provide_demo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        product = tracker.get_slot("product")

        if product:
            dispatcher.utter_message(
                text=f"Công ty hiện có bản demo cho phần mềm {product}. "
                     f"Bạn có muốn mình gửi link demo qua email không?"
            )
        else:
            dispatcher.utter_message(
                text="Bên mình có hỗ trợ demo cho nhiều phần mềm khác nhau. "
                     "Bạn có muốn mình gửi link demo và tài liệu hướng dẫn qua email không?"
            )
        return [SlotSet("email_context", "demo")]

class ActionSaveEmail(Action):
    def name(self):
        return "action_save_email"

    def run(self, dispatcher, tracker, domain):
        email = next(tracker.get_latest_entity_values("email"), None)

        if email:
            dispatcher.utter_message(
                text=f"Mình đã ghi nhận email {email}. Bộ phận kinh doanh sẽ gửi báo giá sớm nhất!"
            )
            dispatcher.utter_message(
                text="Cảm ơn bạn đã quan tâm! 😊"
            )
            return [SlotSet("email", email), SlotSet("email_context", None)]
        else:
            dispatcher.utter_message(
                text="Mình chưa nhận được email của bạn, vui lòng nhập lại nhé."
            )
            return []

class ActionSaveEmailDemo(Action):
    def name(self) -> Text:
        return "action_save_email_demo"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        email = next(tracker.get_latest_entity_values("email"), None)

        if email:
            dispatcher.utter_message(
                text=f"Mình đã ghi nhận email {email}. Bộ phận kinh doanh sẽ gửi link demo sớm nhất!"
            )
            dispatcher.utter_message(
                text="Cảm ơn bạn đã quan tâm sản phẩm của Văn Việt! 😊"
            )
            return [SlotSet("email", email)]
        else:
            dispatcher.utter_message(
                text="Mình chưa nhận được email của bạn, vui lòng nhập lại nhé."
            )
            return []
class ActionTechSupport(Action):
    def name(self) -> Text:
        return "action_tech_support"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        issue_type = tracker.get_slot("issue_type")
        msg = ""

        if issue_type:
            itype = issue_type.lower()
            if "lỗi phần mềm" in itype:
                msg = "Bạn vui lòng cung cấp thêm thông tin về lỗi phần mềm bạn gặp phải để mình hỗ trợ nhé."
            elif "hướng dẫn sử dụng" in itype:
                msg = "Bạn có thể tham khảo tài liệu hướng dẫn sử dụng trên website hoặc mình có thể gửi qua email cho bạn."
            elif "cập nhật" in itype:
                msg = "Để cập nhật phần mềm, vui lòng truy cập trang quản lý tài khoản hoặc liên hệ bộ phận kỹ thuật để được hỗ trợ."
            else:
                msg = (
                    f"Bạn đang gặp vấn đề về '{issue_type}', đúng không? "
                    "Vui lòng cung cấp thêm chi tiết để mình hỗ trợ tốt hơn."
                )
        else:
            msg = "Bạn cần hỗ trợ kỹ thuật về vấn đề gì? Vui lòng cung cấp thêm thông tin để mình giúp bạn nhé."

        dispatcher.utter_message(text=msg)
        # Reset slot để lần hỏi tiếp theo không bị nhầm
        return [SlotSet("issue_type", None)]
    
class ActionWarrantyPolicy(Action):
    def name(self) -> Text:
        return "action_warranty_policy"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        warranty_item = tracker.get_slot("warranty_item")
        msg = ""

        if warranty_item:
            item = warranty_item.lower()
            if "thời gian" in item:
                msg = "Thời gian bảo hành phần mềm là **12 tháng** kể từ ngày bàn giao."
            elif "thời gian" in item:
                msg = "Thời gian bảo hành phần mềm là **12 tháng** kể từ ngày bàn giao."
            elif "bảo trì" in item:
                msg = "Bên mình có **dịch vụ bảo trì định kỳ miễn phí trong 1 năm đầu**, sau đó có gói bảo trì hàng năm."
            elif "nâng cấp" in item:
                msg = "Trong thời gian bảo hành, phần mềm được **cập nhật và nâng cấp miễn phí**."
            elif "phí" in item or "mất phí" in item:
                msg = "Mọi lỗi kỹ thuật trong thời gian bảo hành đều **được hỗ trợ miễn phí**."
            else:
                msg = (
                    "Công ty có chính sách bảo hành và bảo trì đầy đủ. "
                    
                )
        else:
            msg = (
                "Chính sách bảo hành phần mềm của công ty Văn Việt kéo dài **12 tháng**, "
                "bao gồm hỗ trợ cập nhật và bảo trì miễn phí."
            )

        dispatcher.utter_message(text=msg)
        
        # Reset slot để lần hỏi tiếp theo không bị nhầm
        return [SlotSet("warranty_item", None)]
class ActionPromotionInfo(Action):
    def name(self) -> Text:
        return "action_promotion_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy các slot
        promotion_type = tracker.get_slot("promotion_type")
        promotion_event = tracker.get_slot("promotion_event")
        product = tracker.get_slot("product")

        # Mặc định
        msg = "Hiện tại công ty Văn Việt đang có nhiều chương trình ưu đãi hấp dẫn cho khách hàng và doanh nghiệp."

        # Ưu tiên product nếu có
        if product:
            product_lower = product.lower()
            if "giáo dục" in product_lower:
                msg = f"Phần mềm {product} đang **giảm 15% cho gói giáo dục** và tặng 3 tháng bảo trì."
            elif "erp" in product_lower:
                msg = f"Phần mềm {product} đang **ưu đãi giảm 10%** cho khách hàng mới."
            elif "crm" in product_lower:
                msg = f"Phần mềm {product} hiện đang có **giảm 10% phí bản quyền năm đầu**."
            else:
                msg = f"Phần mềm {product} hiện đang được **giảm giá 10%** và tặng gói bảo trì 6 tháng."
        
        # Nếu có event ưu đãi đặc biệt
        elif promotion_event:
            msg = f"Nhân dịp {promotion_event}, công ty đang có **ưu đãi giảm giá 20%** cho tất cả các sản phẩm phần mềm!"
        
        # Nếu có loại ưu đãi cụ thể
        elif promotion_type:
            ptype = promotion_type.lower()
            if "khách hàng mới" in ptype or "ưu đãi" in ptype:
                msg = "Khách hàng mới được **giảm 15% phí bản quyền năm đầu tiên** và **tặng 3 tháng bảo trì miễn phí**."
            elif "tri ân" in ptype:
                msg = "Chương trình **tri ân khách hàng cũ**: giảm 10% khi gia hạn phần mềm hoặc nâng cấp gói dịch vụ."
            elif "giới thiệu" in ptype:
                msg = "Khi bạn giới thiệu khách hàng mới, bạn sẽ nhận **voucher 1.000.000đ** hoặc 1 tháng sử dụng miễn phí."
            elif "combo" in ptype:
                msg = "Combo phần mềm + dịch vụ triển khai hiện đang **giảm 25%** cho doanh nghiệp nhỏ và vừa."
        
        # Nếu không có thông tin gì → hỏi người dùng
        else:
            msg = "Hiện tại công ty có nhiều chương trình ưu đãi. Bạn muốn biết ưu đãi theo **sản phẩm** hay theo **sự kiện/loại ưu đãi**?"

        dispatcher.utter_message(text=msg)

        # Reset các slot sau khi phản hồi
        return [
            SlotSet("promotion_type", None),
            SlotSet("promotion_event", None),
            SlotSet("product", None)
        ]
class ActionPartnerRequest(Action):
    def name(self):
        return "action_partner_request"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        
        partner_type = tracker.get_slot("partner_type")
        company = tracker.get_slot("company_name")
        field = tracker.get_slot("collab_field")

        if not any([company, partner_type, field]):
            reply = ("Cảm ơn bạn đã quan tâm hợp tác. "
                     "Bạn vui lòng cho chúng tôi xin email để bộ phận kinh doanh liên hệ")
        else:
            parts = ["Cảm ơn bạn"]
            if company:
                parts.append(f"đại diện cho {company}")
            if partner_type:
                parts.append(f"với mong muốn trở thành {partner_type}")
            if field:
                parts.append(f"trong lĩnh vực {field}")
            
            reply = " ".join(parts)
            reply += ". Bạn vui lòng cho chúng tôi xin email để bộ phận kinh doanh liên hệ: contact@vanvietsoft.vn."

        dispatcher.utter_message(text=reply)
        
        return [
            SlotSet("partner_type", None),
            SlotSet("company_name", None),
            SlotSet("collab_field", None)
        ]

class ActionAskRemoteSupport(Action):
    def name(self) -> Text:
        return "action_ask_remote_support"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        remote_tool = tracker.get_slot("remote_tool")

        if remote_tool:
            message = (
                f"Dạ, bên mình có thể hỗ trợ qua {remote_tool}. "
                "Bạn vui lòng gửi ID và mật khẩu để kỹ thuật viên kết nối nhé."
            )
        else:
            message = (
                "Bên mình hỗ trợ remote qua TeamViewer, AnyDesk hoặc UltraViewer. "
                "Bạn có thể cho biết bạn đang dùng phần mềm nào và công cụ remote bạn muốn sử dụng để mình hướng dẫn chi tiết."
            )

        dispatcher.utter_message(text=message)

        # Reset slot để lần hỏi tiếp theo không bị nhầm
        return [SlotSet("remote_tool", None)]


import csv
import os
from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

LOG_FILE = "unrecognized.csv"

def log_unrecognized(utterance: Text, predicted_intent: Optional[Text], confidence: Optional[float]):
    header = ["utterance", "predicted_intent", "confidence"]
    exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(header)
        writer.writerow([utterance, predicted_intent if predicted_intent else "", confidence if confidence else ""])

class ActionHandleFallback(Action):
    def name(self) -> Text:
        return "action_handle_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # read previous fallback count
        fallback_count = tracker.get_slot("fallback_count") or 0
        fallback_count = int(fallback_count) + 1

        last_user_utterance = tracker.latest_message.get("text")
        # best guess intent + confidence if available
        intent = None
        confidence = None
        intent_ranking = tracker.latest_message.get("intent_ranking")
        if intent_ranking and len(intent_ranking) > 0:
            intent = intent_ranking[0].get("name")
            confidence = intent_ranking[0].get("confidence")

        # log for active learning
        try:
            log_unrecognized(last_user_utterance, intent, confidence)
        except Exception as e:
            # don't fail entire action if logging fails
            print(f"[action_handle_fallback] logging failed: {e}")

        # Responses by fallback_count
        if fallback_count == 1:
            # First fallback: ask for clarification
            dispatcher.utter_message(response="utter_fallback_first")
            # optionally ask a targeted clarification
            # you can also ask a specific question depending on context
            return [SlotSet("fallback_count", fallback_count)]
        elif fallback_count == 2:
            # Second fallback: provide suggestions / quick-replies
            buttons = [
                {"title": "Xem sản phẩm", "payload": "/ask_product"},
                {"title": "Yêu cầu báo giá", "payload": "/ask_price"},
                {"title": "Yêu cầu demo", "payload": "/request_demo"},
                {"title": "Hỗ trợ kỹ thuật", "payload": "/support_tech"}
            ]
            dispatcher.utter_message(response="utter_fallback_second", buttons=buttons)
            return [SlotSet("fallback_count", fallback_count)]
        else:
            # Third fallback or more: escalate to human / contact info
            dispatcher.utter_message(response="utter_fallback_third")
            # reset counter after escalation
            return [SlotSet("fallback_count", 0), SlotSet("escalated_from_fallback", True)]
