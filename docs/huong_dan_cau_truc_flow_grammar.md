# Hướng dẫn tạo đúng cấu trúc flow cho bài grammar mới

## 1. Thứ tự các bước trong flow

1. **action: utter_{file_name}_begin**  
   Bước chào mừng đầu tiên.

2. **collect: {file_name}_is_skip_theory**  
   Hỏi người học có muốn bỏ qua phần lý thuyết không.

3. **next:**
    - Nếu bỏ qua lý thuyết: chuyển đến bước thực hành đầu tiên ({file_name}_practice_q1)
    - Nếu không: chuyển đến bước lý thuyết đầu tiên ({file_name}_grammar_1)

4. **id: {file_name}_grammar_1**
    - **action: utter_{file_name}_grammar_1**
    - **next:** hỏi kiểm tra hiểu bài (ask_understand_{file_name}_grammar_1)

5. **id: ask_understand_{file_name}_grammar_1**
    - **collect: {file_name}_understand_1**
    - **next:**
        - Nếu hiểu: sang grammar tiếp theo hoặc ask_practice_{file_name} nếu không có grammar tiếp theo
        - Nếu chưa: giải thích thêm rồi sang grammar tiếp theo hoặc ask_practice_{file_name} nếu không có grammar tiếp theo
6. **id: ask_practice_{file_name}**
    - **collect: {file_name}_practice**
    - **next:**
        - Nếu muốn thực hành: sang practice_q1
        - Nếu không: {file_name}_end_lesson
7. **id: {file_name}_practice_q1**
    - **collect: {file_name}_practice_q1**
    - **next:**
        - Nếu đúng: utter_correct_{file_name}_q1 rồi sang {file_name}_practice_q2 hoặc {file_name}_end_lesson nếu đã làm hết các {file_name}_practice_q
        - Nếu sai: utter_incorrect_{file_name}_q1 rồi sang {file_name}_practice_q2 hoặc {file_name}_end_lesson nếu đã làm hết các {file_name}_practice_q
8. **id: {file_name}_end_lesson**
    - **action: utter_{file_name}_end**
    - **next: END**

## 2. Ví dụ cấu trúc flow tối giản

```yaml
flows:
    grammar_ten_bai:
        description: Mô tả ngắn về bài học.
        steps:
            - action: utter_begin
            - collect: is_skip_theory
              next:
                  - if: slots.is_skip_theory = true
                    then: practice_q1
                  - else: grammar_1
            - id: grammar_1
              action: utter_grammar_1
              next: ask_understand_grammar_1
            - id: ask_understand_grammar_1
              collect: understand_1
              next:
                  - if: slots.understand_1 = true
                    then: ask_practice
                  - else:
                        - action: utter_explain_more_1
                          next: ask_practice
            - id: ask_practice
              collect: practice
              next:
                  - if: slots.practice = true
                    then: practice_q1
                  - else: end_lesson
            - id: practice_q1
              collect: practice_q1
              next:
                  - if: slots.practice_q1 = "a"
                    then:
                        - action: utter_correct_q1
                          next: end_lesson
                  - else:
                        - action: utter_incorrect_q1
                          next: end_lesson
            - id: end_lesson
              action: utter_end
              next: END
```

## 3. Lưu ý

-   collect: abc, thì phải có slot abc và utter_ask_abc (định nghĩa bên domain)

    > ví dụ: collect: practice_q1, thì phải có slot practice_q1 và utter_ask_practice_q1 (định nghĩa bên domain)

-   Flow luôn gồm 2 phần: grammar và practice.
-   Grammar luôn được đánh số thứ tự grammar\_{number}, bao gồm một nội dung lý thuyết nhỏ (sẽ chia bài học thành nhiều grammar để giữ cho cuộc hội thoại không bị dài dòng)
-   1 Grammar sẽ bao gồm:

    -   utter_grammar_1: nội dung lý
    -   understand_1: Slot bool, kiểm tra hiểu bài
    -   utter_explain_more_1: nội dung giải thích thêm nếu chưa hiểu

-   Practice luôn được đánh số thứ tự practice_q{number}, bao gồm nhiều câu hỏi thực hành.
-   practice_q{number} là slot type là categorical, luôn có 3 giá trị: a, b, c.
-   1 practice_q{number} sẽ bao gồm:
    -   utter_ask_practice_q{number}: câu hỏi thực hành (định nghĩa bên domain)
    -   utter_correct_q1
    -   utter_incorrect_q1

# Hướng dẫn tạo đúng cấu trúc domain cho bài grammar mới

## Slots

```yaml
slots:
    is_skip_theory:
        type: bool
        mappings:
            - type: controlled

    # Understand
    understand_1:
        type: bool
        mappings:
            - type: controlled

    # Practice
    practice:
        type: bool
        mappings:
            - type: controlled

    practice_q1:
        type: categorical
        values:
            - a
            - b
            - c
        mappings:
            - type: controlled
```

-   understand_{number} là slot type là bool, kiểm tra hiểu bài
-   practice_q{number} là slot type là categorical, luôn có 3 giá trị: a, b, c.

## Responses

```yaml
# Begin
utter_begin:
    - text: |
          🎓 Welcome to the TOEIC Grammar lesson!
          In this lesson, we'll learn about countable and uncountable nouns.
          Let's get started!
# Ask if skip theory
utter_ask_is_skip_theory:
    - text: |
          🤔 Do you want to skip the theory part and go straight to the practice?
      buttons:
          - title: "Yes"
            payload: "/SetSlots(is_skip_theory=true)"
          - title: "No"
            payload: "/SetSlots(is_skip_theory=false)"
# End
utter_end:
    - text: |
          🎉 Thank you for learning about countable and uncountable nouns!
          I hope you found this helpful.
          Have a great day! 🌟
      image: "https://static.klipy.com/ii/feea28532d9709f5128558f418c779d0/c9/40/StrU5mdz.gif"

# Grammar
utter_grammar_1:
    - text: |
          🍏 **Countable nouns** are nouns you can count one by one.
          Examples:
          - 1 apple, 2 apples
          - book, car, cat
utter_ask_understand_1:
    - text: |
          🤔 Do you clear about this part? 
          (Please answer: **yes** or **no**)
      buttons:
          - title: "Yes"
            payload: "/SetSlots(understand_1=true)"
          - title: "No"
            payload: "/SetSlots(understand_1=false)"
utter_explain_more_1:
    - text: |
          🧮 Countable nouns are things or people you can count individually.
          For example:
          - 1 chair, 2 chairs
          Countable nouns have both singular and plural forms.
      metadata:
          rephrase: True
          rephrase_prompt: |
              You are a TOEIC teacher. Rephrase the response based on {{current_input}}, {{suggested_response}}, and {{history}}.
              Keep the response concise, avoid repetition, and do not add introductory sentences or unnecessary explanations. Use Markdown for formatting (e.g., headers, lists, ...) and emoji if needed.

              Explain more about countable nouns.

              {{history}}
              {{current_input}}
              Suggested AI Response: {{suggested_response}}
              Rephrased AI Response:

# Ask if practice
utter_ask_practice:
    - text: |
          📝 Would you like to try some practice questions?
      buttons:
          - title: "Yes"
            payload: "/SetSlots(practice=true)"
          - title: "No"
            payload: "/SetSlots(practice=false)"

# Practice question 1
utter_ask_practice_q1:
    - text: |
          ❓ **Question 1:** Choose the countable noun from the following:
      buttons:
          - title: "🍏 apple"
            payload: "a"
          - title: "💧 water"
            payload: "b"
          - title: "🍚 rice"
            payload: "c"
utter_correct_q1:
    - text: |
          ✅ Correct! **'apple'** is a countable noun.
utter_incorrect_q1:
    - text: |
          ❌ Not quite. The correct answer is **'apple' (A)** because it can be counted.
```

-   utter_ask_understand_{number} có cấu trúc như sau:

> Luôn phải có utter_ask_understand_{number} và slot understand_{number}, để collect: understand_{number} bên flow hoạt động

```yaml
utter_ask_understand_1:
    - text: |
          🤔 Do you clear about this part? 
          (Please answer: **yes** or **no**)
      buttons:
          - title: "Yes"
            payload: "/SetSlots(understand_1=true)"
          - title: "No"
            payload: "/SetSlots(understand_1=false)"
```

-   utter_ask_practice có cấu trúc như sau:

```yaml
utter_ask_practice:
    - text: |
          📝 Would you like to try some practice questions?
      buttons:
          - title: "Yes"
            payload: "/SetSlots(practice=true)"
          - title: "No"
            payload: "/SetSlots(practice=false)"
```

-   utter_ask_practice_q{number} có cấu trúc như sau:

>  Có thể mở rộng nhiều dạng bài, chọn câu đúng, ... nhưng bên backend vẫn cấu hình đúng cấu trúc a b c bên dưới

```yaml
utter_ask_practice_q1:
    - text: |
          ❓ **Question 1:** Choose the countable noun from the following:
      buttons:
          - title: "🍏 apple"
            payload: "a"
          - title: "💧 water"
            payload: "b"
          - title: "🍚 rice"
            payload: "c"
```

-   utter_explain_more_{number} có cấu trúc như sau:

```yaml
utter_explain_more_1:
    - text: |
          🧮 Countable nouns are things or people you can count individually.
          For example:
          - 1 chair, 2 chairs
          Countable nouns have both singular and plural forms.
      metadata:
          rephrase: True
          rephrase_prompt: |
              You are a TOEIC teacher. Rephrase the response based on {{current_input}}, {{suggested_response}}, and {{history}}.
              Keep the response concise, avoid repetition, and do not add introductory sentences or unnecessary explanations. Use Markdown for formatting (e.g., headers, lists, ...) and emoji if needed.

              Explain more about countable nouns.

              {{history}}
              {{current_input}}
              Suggested AI Response: {{suggested_response}}
              Rephrased AI Response:
```

> Chú ý: rephrase_prompt để hướng dẫn LLM tạo nội dung giải thích thêm. Giữ nguyên format của prompt trên chỉ thay đổi `Explain more about countable nouns.`

> Chú ý trong mỗi response, có thể add thêm image, nếu thực sự phù hợp
> danh sách image lấy từ `assets/gif_data.json`, `assets/meme_data.json`, `assets/sticker_data.json` nội dung trong file sẽ là 

```json
{
                "id": 2773430115486026,
                "slug": "sparkles-glitter-sticker",
                "title": "Sparkles Glitter Sticker",
                "blur_preview": "",
                "file": {
                    "hd": {
                        "gif": {
                            "url": "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/30/9a/txBGxv21.gif",
                            "width": 498,
                            "height": 498,
                            "size": 682311
                        },
                        "webp": {
                            "url": "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/30/9a/lA0mT7mA.webp",
                            "width": 498,
                            "height": 498,
                            "size": 519666
                        }
                    }
                },
                "type": "sticker"
            },
```

> dựa vào title đề xác định được image nào phù hợp

> cấu trúc để thêm image như sau:

```yaml
utter_end:
    - text: |
        🎉 Thank you for learning about countable and uncountable nouns!
        I hope you found this helpful.
        Have a great day! 🌟
      buttons:
        - title: "Yes"
          payload: "/SetSlots(is_skip_theory=true)"
        - title: "No"
          payload: "/SetSlots(is_skip_theory=false)"
      image: "https://static.klipy.com/ii/feea28532d9709f5128558f418c779d0/c9/40/StrU5mdz.gif"
```

# Lưu ý

- Dựa vào nội dung grammar sẽ được cung cấp, tạo các `grammar_{number}` và `ask_understand_grammar_{number}` sẽ là các đoạn hội thoại gởi đến người học.
- Giữ cho nội dung của `utter_grammar_{number}` ngắn gọn, không quá dài, có chủ đề rõ ràng.
- Không nên chia thành quá nhiều `grammar_{number}`, nên tạo khoảng từ 10-20. 

- Nên tạo khoảng 10-20 câu hỏi `practice_q{number}` bao quát tất cả các trường hợp nhất có thể.