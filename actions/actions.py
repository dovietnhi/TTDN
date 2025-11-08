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
                dispatcher.utter_message(text="Phần mềm hóa đơn điện tử của V2S tuân thủ quy định của Tổng cục Thuế, dễ tích hợp với các hệ thống khác.")
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
        return [SlotSet("product", None)]

class ActionSaveEmail(Action):
    def name(self):
        return "action_save_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        email = next(tracker.get_latest_entity_values("email"), None)
        if email:
            dispatcher.utter_message(text=f"Mình đã ghi nhận email {email}. Bộ phận kinh doanh sẽ gửi báo giá sớm nhất!")
            dispatcher.utter_message(text="Cảm ơn bạn đã quan tâm! 😊")
        else:
            dispatcher.utter_message(text="Mình chưa nhận được email của bạn, vui lòng nhập lại nhé.")
        return []
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
        return [SlotSet("product", None)]

class ActionSaveEmailDemo(Action):
    def name(self):
        return "action_save_email_demo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        email = next(tracker.get_latest_entity_values("email"), None)
        if email:
            dispatcher.utter_message(
                text=f"Mình đã ghi nhận email {email}. Bộ phận kinh doanh sẽ gửi link demo sớm nhất!"
            )
            dispatcher.utter_message(
                text="Cảm ơn bạn đã quan tâm sản phẩm của Văn Việt! 😊"
            )
        else:
            dispatcher.utter_message(text="Mình chưa nhận được email của bạn, vui lòng nhập lại nhé.")
        return []
class ActionTechSupport(Action):
    def name(self) -> Text:
        return "action_tech_support"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        issue_type = tracker.get_slot("issue_type")

        if issue_type:
            issue_type = issue_type.lower()
            if "lỗi phần mềm" in issue_type:
                msg = "Bạn vui lòng cung cấp thêm thông tin về lỗi phần mềm bạn gặp phải để mình hỗ trợ nhé."
            elif "hướng dẫn sử dụng" in issue_type:
                msg = "Bạn có thể tham khảo tài liệu hướng dẫn sử dụng trên website của chúng tôi hoặc mình có thể gửi qua email cho bạn."
            elif "cập nhật" in issue_type:
                msg = "Để cập nhật phần mềm, bạn vui lòng truy cập vào trang quản lý tài khoản hoặc liên hệ bộ phận kỹ thuật để được hỗ trợ."
            else:
                msg = f"Bạn đang gặp vấn đề về '{issue_type}', đúng không? Vui lòng cung cấp thêm chi tiết để mình hỗ trợ tốt hơn."

        else:
            msg = "Bạn cần hỗ trợ kỹ thuật về vấn đề gì? Vui lòng cung cấp thêm thông tin để mình giúp bạn nhé."

        dispatcher.utter_message(text=msg)
        return [SlotSet("issue_type", None)]
    
class ActionWarrantyPolicy(Action):
    def name(self) -> Text:
        return "action_warranty_policy"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        warranty_item = tracker.get_slot("warranty_item")

        # ✅ Xử lý logic tùy theo entity mà người dùng hỏi
        if warranty_item:
            warranty_item = warranty_item.lower()
            if "thời gian" in warranty_item:
                msg = "Thời gian bảo hành phần mềm là **12 tháng** kể từ ngày bàn giao."
            elif "bảo trì" in warranty_item:
                msg = "Bên mình có **dịch vụ bảo trì định kỳ miễn phí trong 1 năm đầu**, sau đó có gói bảo trì hàng năm."
            elif "nâng cấp" in warranty_item:
                msg = "Trong thời gian bảo hành, phần mềm được **cập nhật và nâng cấp miễn phí**."
            elif "phí" in warranty_item or "mất phí" in warranty_item:
                msg = "Mọi lỗi kỹ thuật trong thời gian bảo hành đều **được hỗ trợ miễn phí**."
            else:
                msg = f"Công ty có chính sách bảo hành và bảo trì đầy đủ. Bạn đang hỏi về '{warranty_item}', đúng không?"

        else:
            msg = "Chính sách bảo hành phần mềm của công ty Văn Việt kéo dài **12 tháng**, có hỗ trợ cập nhật và bảo trì miễn phí."

        dispatcher.utter_message(text=msg)
        return [SlotSet("warranty_item", None)]
class ActionPromotionInfo(Action):
    def name(self) -> Text:
        return "action_promotion_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        promotion_type = tracker.get_slot("promotion_type")
        promotion_event = tracker.get_slot("promotion_event")
        product = tracker.get_slot("product")

        # Mặc định
        msg = "Hiện tại công ty Văn Việt đang có nhiều chương trình ưu đãi hấp dẫn cho khách hàng mới và doanh nghiệp."

        # Xử lý chi tiết
        if promotion_event:
            msg = f"Nhân dịp {promotion_event}, công ty đang có **ưu đãi giảm giá 20%** cho tất cả các sản phẩm phần mềm!"
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
        elif product:
            msg = f"Phần mềm {product} hiện đang được **giảm giá 10%** và tặng gói bảo trì 6 tháng."

        dispatcher.utter_message(text=msg)
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

        reply = f"Cảm ơn bạn"
        if company:
            reply += f" đại diện cho {company}"
        if partner_type:
            reply += f" với mong muốn trở thành {partner_type}"
        if field:
            reply += f" trong lĩnh vực {field}"

        reply += ". Bộ phận kinh doanh của chúng tôi sẽ liên hệ sớm nhất qua email contact@vanvietsoft.vn."

        dispatcher.utter_message(text=reply)
        return [
            SlotSet("partner_type", None),
            SlotSet("company_name", None),
            SlotSet("collab_field", None)
        ]
class ActionAskRemoteSupport(Action):
    def name(self):
        return "action_ask_remote_support"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        
        remote_tool = tracker.get_slot("remote_tool")
        if remote_tool:
            message = f"Dạ, bên mình có thể hỗ trợ qua {remote_tool}. Bạn vui lòng gửi ID và mật khẩu để kỹ thuật viên kết nối nhé."
        else:
            message = (
                "Bên mình có hỗ trợ remote qua TeamViewer, AnyDesk hoặc UltraViewer. "
                "Bạn vui lòng cho biết bạn đang dùng phần mềm nào để mình hỗ trợ phù hợp nhé."
            )

        dispatcher.utter_message(text=message)
        return [SlotSet("remote_tool", None)]
