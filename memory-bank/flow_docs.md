# Rasa Pro Flow Design: Best Practices & Reference

## 1. Overview of Flows in Rasa Pro

A **flow** in Rasa Pro (CALM) defines the business logic for a user goal, such as booking a flight or looking up a word. Flows are written in YAML and focus on logic, not every possible conversation path.

### Key Properties of a Flow
| Property         | Description                                                                                 |
|------------------|---------------------------------------------------------------------------------------------|
| id               | Unique identifier (alphanumeric, underscores, hyphens, not starting with hyphen)            |
| description      | Short summary of the flow's purpose (required, used by Dialogue Understanding)              |
| nlu_trigger      | (Optional) List of intents that can start the flow                                          |
| if (flow guards) | (Optional) Condition for starting the flow                                                  |
| persisted_slots  | (Optional) List of slots to persist after the flow ends                                     |
| steps            | List of steps: action, collect, call, link, set_slots, noop                                 |

---

## 2. Using Conditions in Flows

Conditions control the flow logic and can be used in:
- **Flow Guards**: To decide if a flow can start
- **next** field: To branch after a step
- **Rejections in collect**: To validate slot values

### Condition Syntax
- Use natural language logic: `and`, `or`, `not`, `>`, `>=`, `<`, `<=`, `=`, `!=`, `is`, `is not`, `contains`, `matches`
- **Namespaces:**
  - `slots.` for slot values (e.g., `slots.age`)
  - `context.` for dialogue context (e.g., `context.current_date`)
- Conditions are evaluated by the `pypred` library

**Example:**
```yaml
steps:
  - collect: age
    next:
      - if: slots.age < 18
        then: too_young_step
      - else: old_enough_step
  - id: too_young_step
    action: utter_too_young
  - id: old_enough_step
    action: utter_old_enough
```

---

## 3. Starting Flows

Flows can be started by:
- **LLM-based Command Generators**
- **NLUCommandAdapter** (using `nlu_trigger` intents)
- **Flow Guards** (using `if`)

**Example NLU Trigger:**
```yaml
flows:
  my_flow:
    description: "A flow triggered with greet intent"
    nlu_trigger:
      - intent: greet
        confidence_threshold: 0.8
    steps:
      - action: utter_greet
```

**Example Flow Guard:**
```yaml
flows:
  my_flow:
    description: "A flow with guards"
    if: slots.authenticated AND slots.email_verified
    steps:
      - action: my_action
```

---

## 4. Sample Flow: Book a Flight

```yaml
flows:
  book_flight:
    description: Book a flight for the user
    nlu_trigger:
      - intent: book_flight
    steps:
      - id: collect_flight_info
        collect: [departure, arrival, flight_date]
        description: Collect flight details
        next:
          - if: slots.flight_date > context.current_date
            then: confirm_booking
          - else: invalid_date
      - id: confirm_booking
        action: action_confirm_booking
      - id: invalid_date
        action: utter_invalid_date
        next: collect_flight_info
```
**Explanation:**
- The flow starts with the `book_flight` intent.
- Collects departure, arrival, and flight_date slots.
- Branches based on whether the flight date is valid.
- Uses step IDs for branching.

---

## 5. Checklist for Reviewing & Fixing Flows
- [ ] Each flow has a unique `id` and clear `description`.
- [ ] All steps use valid types: `action`, `collect`, `call`, `link`, `set_slots`, `noop`.
- [ ] Branching uses `next:` with `if`, `then`, and (optionally) `else`, referencing step IDs.
- [ ] All slots used in conditions are prefixed with `slots.`.
- [ ] All referenced step IDs exist in the flow.
- [ ] `nlu_trigger` intents are defined in the domain and NLU data.
- [ ] No nested `next:` blocks; all branching is flat and references step IDs.

---

## 6. Common Errors & Troubleshooting
- **Missing or duplicate flow ID:** Ensure each flow has a unique `id`.
- **Invalid step type:** Only use supported step types.
- **Branching errors:** Use `next:` after a step, not as a top-level step. Reference step IDs.
- **Condition syntax errors:** Use correct namespaces and operators.
- **Slot not saved:** Define slots in the domain and collect/set them in the flow.
- **Flow not starting:** Check `nlu_trigger` and `if` guard logic.
- **Infinite loops or dead ends:** Ensure all branches lead to valid steps or END.

---

## 7. References
- [Rasa Pro: Flows](https://rasa.com/docs/reference/primitives/flows)
- [Rasa Pro: Conditions](https://rasa.com/docs/reference/primitives/conditions)
- [Rasa Pro: Starting Flows](https://rasa.com/docs/reference/primitives/starting-flows)
- [Rasa Pro: Writing Flows](https://rasa.com/docs/pro/build/writing-flows) 