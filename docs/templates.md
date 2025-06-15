```yaml
flows:
  countable_uncountable_nouns_grammar:
    description: Learn about countable and uncountable nouns.
    steps:
      - action: utter_begin
      - collect: is_skip_theory
        next:
          - if: slots.is_skip_theory = true
            # Go to practice question 1
            then: practice_q1
            # Go to grammar theory countable 1
          - else: grammar_1

      # Countable Nouns Theory (split into granular steps)
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

      

      # # Practice and End (unchanged)
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

```yaml
version: "3.1"

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

responses:
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