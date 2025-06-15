# Kiến Thức Cốt Lõi Khi Xây Dựng Chatbot Với Rasa Pro (Có Ví Dụ Thực Tế)

## 1. Flow trong Rasa Pro
### 1.1. Flow là gì?
Flow là tập hợp các bước (steps) mô tả logic nghiệp vụ để hoàn thành một mục tiêu cụ thể (ví dụ: tra cứu từ, xác thực, giải thích bài tập). Flow giúp tách biệt logic nghiệp vụ khỏi các tình huống hội thoại linh tinh, giúp code rõ ràng, dễ bảo trì.

### 1.2. Cấu trúc file flow
Mỗi flow là một mục trong file YAML (thường nằm ở `data/flows/`).

**Ví dụ: Flow tra cứu định nghĩa từ**
```yaml
flows:
  get_word_definition:
    description: Lấy định nghĩa của một từ tiếng Anh
    steps:
      - collect: word
        description: Từ cần tra cứu
      - collect: get_word_definition_confirmation
        ask_before_filling: true
        next:
          - if: "slots.get_word_definition_confirmation is not true"
            then:
              - action: utter_get_word_definition_cancelled
                next: END
          - else: get_word_definition
      - id: get_word_definition
        action: get_word_definition
        next:
          - if: "slots.word_definition = 'data_not_present'"
            then:
              - action: utter_word_not_found
                next: END
          - else:
              - action: utter_return_definition_word
                next: END
```
**Giải thích:**
- `collect: word`: Thu thập từ cần tra cứu, lưu vào slot `word`.
- `collect: get_word_definition_confirmation`: Hỏi xác nhận trước khi lấy nghĩa.
- `if ... then ... else ...`: Rẽ nhánh logic dựa vào giá trị slot.
- `action: get_word_definition`: Gọi custom action để lấy nghĩa từ.
- `END`: Kết thúc flow.

### 1.3. Các lệnh thường dùng trong flow
- `collect`: Thu thập thông tin từ user, lưu vào slot. Có thể thêm `ask_before_filling: true` để xác nhận.
- `action`: Gọi action (utter_ hoặc custom action Python).
- `set_slots`: Đặt lại giá trị slot (ví dụ: reset slot).
- `call`/`link`: Gọi flow khác (subflow hoặc follow-up).
- `if/then/else`: Điều kiện rẽ nhánh.
- `force_slot_filling: true`: Bắt buộc phải điền slot này trước khi làm việc khác.
- `id`: Đặt tên cho bước để tham chiếu.
- `next`: Chỉ định bước tiếp theo.
- `END`: Kết thúc flow.

**Ví dụ: Flow xác thực người dùng**
```yaml
flows:
  authenticate_user:
    description: Xác thực người dùng
    steps:
      - collect: username
        description: Tên đăng nhập
      - collect: password
        description: Mật khẩu
        force_slot_filling: true
      - action: action_authenticate
        next:
          - if: "slots.user_authenticated is true"
            then:
              - action: utter_login_success
                next: END
          - else:
              - action: utter_login_failed
                next: END
```

### 1.4. Gọi flow lồng nhau (subflow)
```yaml
flows:
  session_start:
    description: Khi bắt đầu session mới
    steps:
      - call: greet_on_connect

  greet_on_connect:
    description: Chào khi user kết nối
    steps:
      - action: utter_greet_on_connect
```

### 1.5. Sử dụng patterns (system flows)
Patterns là các flow mẫu xử lý các tình huống như cancel, clarification, repeat... Bạn chỉ cần gọi hoặc để assistant tự động sử dụng khi cần.

**Ví dụ:**
```yaml
flows:
  get_word_definition:
    steps:
      - collect: word
      - call: pattern_clarification
      - action: get_word_definition
```

### 1.6. Giải thích chi tiết các lệnh thường dùng trong flow (Có ví dụ)

#### 1.6.1. `collect`
**Mục đích:** Thu thập thông tin từ người dùng, lưu vào slot.

**Ví dụ:**
```yaml
- collect: email
  description: Địa chỉ email của người dùng
```
**Giải thích:** Khi đến bước này, bot sẽ hỏi user nhập email và lưu vào slot `email`.

#### 1.6.2. `action`
**Mục đích:** Gọi một action, có thể là utter_ (trả lời nhanh) hoặc custom action (Python).

**Ví dụ:**
```yaml
- action: utter_greet
```
**Giải thích:** Bot sẽ gửi response `utter_greet` đã định nghĩa trong domain.yml.

**Ví dụ custom action:**
```yaml
- action: action_get_weather
```
**Giải thích:** Gọi hàm Python tên `action_get_weather` trong thư mục actions/.

#### 1.6.3. `set_slots`
**Mục đích:** Đặt lại giá trị cho một hoặc nhiều slot.

**Ví dụ:**
```yaml
- set_slots:
    - email: null
    - user_authenticated: false
```
**Giải thích:** Reset slot `email` về rỗng, đặt slot `user_authenticated` về false.

#### 1.6.4. `call` và `link`
**Mục đích:** Gọi flow khác (subflow hoặc follow-up).

**Ví dụ:**
```yaml
- call: authenticate_user
```
**Giải thích:** Chuyển sang flow `authenticate_user` và thực hiện các bước trong đó.

**Ví dụ:**
```yaml
- link: collect_feedback
```
**Giải thích:** Sau khi xong flow hiện tại, sẽ chuyển tiếp sang flow `collect_feedback`.

#### 1.6.5. `if/then/else` (Điều kiện rẽ nhánh)
**Mục đích:** Kiểm tra điều kiện và rẽ nhánh logic.

**Ví dụ:**
```yaml
- collect: user_authenticated
  next:
    - if: not slots.user_authenticated
      then:
        - action: utter_ask_for_login
        - link: authenticate_user
```
**Giải thích:** Nếu slot `user_authenticated` chưa được xác thực, bot sẽ hỏi đăng nhập và chuyển sang flow xác thực.

#### 1.6.6. `next`
**Mục đích:** Chỉ định bước tiếp theo sau khi thực hiện xong action/collect/flow.

**Ví dụ:**
```yaml
- action: action_check_order
  next:
    - if: slots.order_found is true
      then:
        - action: utter_order_details
          next: END
    - else:
        - action: utter_order_not_found
          next: END
```
**Giải thích:** Sau khi kiểm tra đơn hàng, nếu tìm thấy sẽ trả về chi tiết, không thì báo không tìm thấy.

#### 1.6.7. `END`
**Mục đích:** Kết thúc flow hiện tại, trả quyền điều khiển về flow trước đó (nếu có).

**Ví dụ:**
```yaml
- action: utter_goodbye
  next: END
```
**Giải thích:** Sau khi chào tạm biệt, flow kết thúc.

#### 1.6.8. `id`
**Mục đích:** Đặt tên cho một bước trong flow để tham chiếu ở chỗ khác (thường dùng với next hoặc điều kiện phức tạp).

**Ví dụ:**
```yaml
- id: check_user
  action: action_check_user
```
**Giải thích:** Bước này có thể được tham chiếu ở các bước tiếp theo bằng id `check_user`.

#### 1.6.9. `force_slot_filling`
**Mục đích:** Bắt buộc phải điền slot này trước khi làm việc khác (không bị ngắt bởi các lệnh khác).

**Ví dụ:**
```yaml
- collect: feedback
  force_slot_filling: true
```
**Giải thích:** Bot sẽ chỉ tập trung hỏi cho đến khi user nhập xong feedback.

#### 1.6.10. `ask_before_filling`
**Mục đích:** Hỏi xác nhận trước khi lưu giá trị vào slot.

**Ví dụ:**
```yaml
- collect: phone_number
  ask_before_filling: true
```
**Giải thích:** Sau khi user nhập số điện thoại, bot sẽ xác nhận lại trước khi lưu slot.

---

## 2. Response (Trả lời)
### 2.1. Định nghĩa response
Response được định nghĩa trong `domain.yml` hoặc `responses.yml` dưới key `responses`. Mỗi response thường bắt đầu bằng `utter_`.

**Ví dụ:**
```yaml
responses:
  utter_greet:
    - text: "Xin chào! Tôi có thể giúp gì cho bạn?"
  utter_cheer_up:
    - text: "Đây là meme cho bạn vui lên nhé!"
      image: "https://i.imgur.com/nGF1K8f.jpg"
  utter_ask_type:
    - text: "Bạn muốn tra cứu từ hay giải bài tập?"
      buttons:
        - title: "Tra từ"
          payload: '/inform{"task": "lookup"}'
        - title: "Giải bài tập"
          payload: '/inform{"task": "exercise"}'
```
**Giải thích:**
- `text`: Nội dung trả lời.
- `image`: Trả về hình ảnh/meme/gif.
- `buttons`: Trả về các lựa chọn nhanh cho user.

### 2.2. Sử dụng biến trong response
Bạn có thể chèn giá trị slot vào text bằng `{slot_name}`.
```yaml
responses:
  utter_hello_name:
    - text: "Chào {name}, bạn cần gì?"
```

### 2.3. Đa dạng hóa response
Khai báo nhiều biến thể để bot trả lời tự nhiên hơn.
```yaml
responses:
  utter_greet:
    - text: "Xin chào!"
    - text: "Chào bạn!"
    - text: "Hello!"
```

---

## 3. Đa Ngôn Ngữ (Translation)
### 3.1. Định nghĩa response đa ngôn ngữ
```yaml
responses:
  utter_ask_callback:
    - text: "Bạn có muốn gọi lại không?"
      translation:
        en: "Would you like a callback?"
        fr: "Souhaitez-vous un rappel?"
```

### 3.2. Sử dụng slot ngôn ngữ
Bạn có thể dùng slot `language` để điều khiển ngôn ngữ trả lời.

---

## 4. Assistant Memory (Slots)
### 4.1. Định nghĩa slot
```yaml
slots:
  name:
    type: text
  user_authenticated:
    type: bool
    initial_value: false
```

### 4.2. Sử dụng slot trong flow và response
- Thu thập slot bằng `collect` trong flow.
- Dùng slot để điều kiện hóa logic hoặc chèn vào response.

---

## 5. Custom Actions
### 5.1. Viết custom action
Tạo file Python trong thư mục `actions/`.
```python
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetWordDefinition(Action):
    def name(self):
        return "get_word_definition"

    def run(self, dispatcher, tracker, domain):
        word = tracker.get_slot("word")
        # Gọi API hoặc tra cứu DB ở đây
        definition = "Định nghĩa mẫu cho từ: " + word
        dispatcher.utter_message(text=definition)
        return []
```

### 5.2. Trả về rich content từ custom action
```python
dispatcher.utter_message(text="Đây là meme cho bạn!", image="https://i.imgur.com/nGF1K8f.jpg")
```

---

## 6. Assistant Tone (Phong cách trả lời)
Bạn có thể định nghĩa nhiều response với tone khác nhau, hoặc dùng slot để điều chỉnh tone động.

**Ví dụ:**
```yaml
responses:
  utter_greet_friendly:
    - text: "Chào bạn, mình giúp gì được cho bạn nè? 😊"
  utter_greet_formal:
    - text: "Xin chào quý khách, tôi có thể hỗ trợ gì cho bạn?"
```

---

## 7. Conversation Patterns (Patterns)
Patterns là các flow mẫu xử lý các tình huống như cancel, clarification, repeat...

**Ví dụ sử dụng pattern clarification:**
```yaml
flows:
  get_info:
    steps:
      - collect: info
      - call: pattern_clarification
      - action: process_info
```

---

## 8. Lưu Ý Thực Tế
- Luôn kiểm tra log khi gặp lỗi (docker logs, rasa shell, ...).
- Đảm bảo client (web, chat app) hỗ trợ hiển thị image/gif nếu muốn gửi meme.
- Không commit file `.env` hoặc thông tin nhạy cảm lên git.

---

**Tài liệu này giúp bạn nắm vững các thành phần cốt lõi của Rasa Pro, có ví dụ thực tế, dễ áp dụng cho dự án!** 