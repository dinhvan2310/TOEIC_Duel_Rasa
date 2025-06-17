import yaml
import json
import sys
import random
import os

def generate_slots(topic_name, num_grammar, num_practice):
    slots = {
        f"{topic_name}_is_start": {
            "type": "bool",
            "mappings": [{"type": "controlled"}]
        },
        f"{topic_name}_is_skip_theory": {
            "type": "bool",
            "mappings": [{"type": "controlled"}]
        },
        f"{topic_name}_practice": {
            "type": "bool",
            "mappings": [{"type": "controlled"}]
        }
    }
    for i in range(1, num_grammar + 1):
        slots[f"{topic_name}_understand_{i}"] = {
            "type": "bool",
            "mappings": [{"type": "controlled"}]
        }
    for i in range(1, num_practice + 1):
        slots[f"{topic_name}_practice_q{i}"] = {
            "type": "categorical",
            "values": ["a", "b", "c"],
            "mappings": [{"type": "controlled"}]
        }
    return slots

def generate_grammar_yml(topic_name, grammars, practices, output_file):
    incorrect_image = [
        "https://static.klipy.com/ii/3bbfac09dcb32c2b1e87ad063c4ac16e/5d/05/AuRALdGY.gif",
        "https://static.klipy.com/ii/b34001f2c30672cdcb3d906c28815404/7f/be/Br9T2Vr9.png",
        "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/59/cb/TZKBkz6k.gif",
        "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/a9/1a/HSGgoGTj.gif",
        "https://static.klipy.com/ii/feea28532d9709f5128558f418c779d0/d6/c9/kKEmDTpE.gif",
    ]
    
    data = {'version': '3.1'}
    data['slots'] = generate_slots(topic_name, len(grammars), len(practices))
    responses = {}
    # Add begin utterance
    responses[f"utter_{topic_name}_begin"] = [
        {"text": f"🚀 Let's start learning about {topic_name.replace('_', ' ')}!, (you can ask me to use Vietnamese for this lesson if you want)"}
    ]
    # Add ask is_start utterance
    responses[f"utter_ask_{topic_name}_is_start"] = [
        {"text": f"Are you sure you want to learn about {topic_name.replace('_', ' ')}? 🤔",
         "buttons": [
             {"title": "Yes", "payload": f"/SetSlots({topic_name}_is_start=true)"},
             {"title": "No", "payload": f"/SetSlots({topic_name}_is_start=false)"}
         ]}
    ]
    # Add ask is_skip_theory utterance
    responses[f"utter_ask_{topic_name}_is_skip_theory"] = [
        {"text": f"Would you like to skip the theory and go straight to practice?",
         "buttons": [
             {"title": "Yes, skip theory", "payload": f"/SetSlots({topic_name}_is_skip_theory=true)"},
             {"title": "No, show me the theory", "payload": f"/SetSlots({topic_name}_is_skip_theory=false)"}
         ]}
    ]
    # Add ask practice utterance
    responses[f"utter_ask_{topic_name}_practice"] = [
        {"text": f"📝 Would you like to try some practice questions?",
         "buttons": [
             {"title": "Yes", "payload": f"/SetSlots({topic_name}_practice=true)"},
             {"title": "No", "payload": f"/SetSlots({topic_name}_practice=false)"}
         ]}
    ]
    # Grammar responses
    for g in grammars:
        # Grammar short
        resp_grammar = {"text": g["short"]}
        if g.get("short_vi"):
            resp_grammar["translation"] = {"vi": g["short_vi"]}
        responses[f"utter_{topic_name}_grammar_{g['index']}"] = [resp_grammar]
        # Grammar detail
        resp_detail = {"text": g["detail"]}
        if g.get("detail_vi"):
            resp_detail["translation"] = {"vi": g["detail_vi"]}
        responses[f"utter_{topic_name}_explain_more_{g['index']}"] = [resp_detail]
        # Add ask understand for each grammar point
        responses[f"utter_ask_{topic_name}_understand_{g['index']}"] = [
            {"text": "🤔 Do you want to get more details about this?",
             "buttons": [
                 {"title": "Yes", "payload": f"/SetSlots({topic_name}_understand_{g['index']}=true)"},
                 {"title": "No", "payload": f"/SetSlots({topic_name}_understand_{g['index']}=false)"}
             ]}
        ]
    # Practice responses
    for p in practices:
        # Question
        responses[f"utter_ask_{topic_name}_practice_q{p['index']}"] = [{
            "text": f"❓ **Question {p['index']}:** {p['question']}",
            "buttons": [
                {"title": p["options"][0], "payload": f"/SetSlots({topic_name}_practice_q{p['index']}=a)"},
                {"title": p["options"][1], "payload": f"/SetSlots({topic_name}_practice_q{p['index']}=b)"},
                {"title": p["options"][2], "payload": f"/SetSlots({topic_name}_practice_q{p['index']}=c)"},
            ]
        }]
        # Correct/Incorrect
        responses[f"utter_{topic_name}_correct_q{p['index']}"] = [{
            "text": p["correct_text"]
        }]
        incorrect_resp = {"text": p["incorrect_text"]}
        if random.random() < 0.4:
            incorrect_resp["image"] = random.choice(incorrect_image)
        responses[f"utter_{topic_name}_incorrect_q{p['index']}"] = [incorrect_resp]
    # Add end utterance
    responses[f"utter_{topic_name}_end"] = [
        {
            "text": f"🎉 Thank you for learning about {topic_name.replace('_', ' ')}! I hope you found this helpful. Have a great day! 🎉",
            "image": "https://static.klipy.com/ii/feea28532d9709f5128558f418c779d0/c9/40/StrU5mdz.gif"
        },
        {
            "text": "🎉 Great job finishing this lesson! Keep up the good work and see you next time! 🎉",
            "image": "https://static.klipy.com/ii/feea28532d9709f5128558f418c779d0/c9/40/StrU5mdz.gif"
        },
        {
            "text": "👏 You did amazing! Thanks for learning with me. Have a wonderful day!",
            "image": "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/89/0c/eVPjF1Tc.gif"
        },
        {
            "text": "🌟 Congratulations on completing the topic! Hope you enjoyed it. See you soon!",
            "image": "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/30/9a/txBGxv21.gif"
        },
        {
            "text": "🎊 Well done! You've learned something new today. Take care and keep practicing!",
            "image": "https://static.klipy.com/ii/925f17378dd1893b674a723c07535afe/92/6e/GkcD7BLA.gif"
        },
        {
            "text": "✨ That's a wrap! Thanks for joining this lesson. Wishing you lots of success!",
            "image": "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/61/ec/cC1mwNmR.gif"
        },
        {
            "text": "🎈 Thank you for your effort! Hope you had fun learning. See you in the next lesson!",
            "image": "https://static.klipy.com/ii/c3a19a0b747a76e98651f2b9a3cca5ff/c5/d0/EvUga4Gv.gif"
        },
        {
            "text": "🚀 You're awesome! Thanks for joining this lesson. Keep shining and see you soon!",
            "image": "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/30/9a/txBGxv21.gif"
        },
        {
            "text": "🥳 Lesson complete! Hope you had fun. Don't forget to practice and smile every day!",
            "image": "https://static.klipy.com/ii/925f17378dd1893b674a723c07535afe/92/6e/GkcD7BLA.gif"
        },
        {
            "text": "💡 You did it! Keep learning and growing. Until next time!",
            "image": "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/61/ec/cC1mwNmR.gif"
        },
        {
            "text": "😃 Thanks for your hard work! Wishing you lots of success ahead.",
            "image": "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/89/0c/eVPjF1Tc.gif"
        },
        {
            "text": "🍀 Good luck on your learning journey! See you in the next lesson.",
            "image": "https://static.klipy.com/ii/c3a19a0b747a76e98651f2b9a3cca5ff/c5/d0/EvUga4Gv.gif"
        },
        {
            "text": "🦸‍♂️ You're a grammar hero! Thanks for learning with me.",
            "image": "https://static.klipy.com/ii/feea28532d9709f5128558f418c779d0/d6/c9/kKEmDTpE.gif"
        },
        {
            "text": "📚 Another topic mastered! Proud of you. See you again soon!",
            "image": "https://static.klipy.com/ii/c98c4a4935d23b95805f0befee091d8a/30/9a/txBGxv21.gif"
        }
    ]
    data['responses'] = responses
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"Đã sinh file {output_file}")

def generate_grammar_flow_yml(topic_name, grammars, practices, output_file):
    flow = {
        'flows': {
            f'{topic_name}_grammar': {
                'description': f'Learn about {topic_name.replace("_", " ")}',
                'steps': []
            }
        }
    }
    steps = flow['flows'][f'{topic_name}_grammar']['steps']
    # Initial is_start step
    steps.append({
        'collect': f'{topic_name}_is_start',
        'next': [
            {'if': f'slots.{topic_name}_is_start = true', 'then': [
                {'action': f'utter_{topic_name}_begin', 'next': f'{topic_name}_ask_is_skip_theory'}
            ]},
            {'else': 'END'}
        ]
    })
    # Skip theory
    steps.append({
        'id': f'{topic_name}_ask_is_skip_theory',
        'collect': f'{topic_name}_is_skip_theory',
        'next': [
            {'if': f'slots.{topic_name}_is_skip_theory = true', 'then': f'{topic_name}_practice_q1'},
            {'else': f'{topic_name}_grammar_1'}
        ]
    })
    # Grammar steps
    for i, g in enumerate(grammars, 1):
        steps.append({
            'id': f'{topic_name}_grammar_{i}',
            'action': f'utter_{topic_name}_grammar_{i}',
            'next': f'{topic_name}_ask_understand_grammar_{i}'
        })
        steps.append({
            'id': f'{topic_name}_ask_understand_grammar_{i}',
            'collect': f'{topic_name}_understand_{i}',
            'next': [
                {'if': f'slots.{topic_name}_understand_{i} = false', 'then': f'{topic_name}_grammar_{i+1}' if i < len(grammars) else f'{topic_name}_ask_practice'},
                {'else': [
                    {'action': f'utter_{topic_name}_explain_more_{i}', 'next': f'{topic_name}_grammar_{i+1}' if i < len(grammars) else f'{topic_name}_ask_practice'}
                ]}
            ]
        })
    # Ask practice
    steps.append({
        'id': f'{topic_name}_ask_practice',
        'collect': f'{topic_name}_practice',
        'next': [
            {'if': f'slots.{topic_name}_practice = true', 'then': f'{topic_name}_practice_q1'},
            {'else': f'{topic_name}_end_lesson'}
        ]
    })
    # Practice questions
    for i, p in enumerate(practices, 1):
        next_step = f'{topic_name}_practice_q{i+1}' if i < len(practices) else f'{topic_name}_end_lesson'
        steps.append({
            'id': f'{topic_name}_practice_q{i}',
            'collect': f'{topic_name}_practice_q{i}',
            'next': [
                {'if': f'slots.{topic_name}_practice_q{i} = "{p["correct"]}"', 'then': [
                    {'action': f'utter_{topic_name}_correct_q{i}', 'next': next_step}
                ]},
                {'else': [
                    {'action': f'utter_{topic_name}_incorrect_q{i}', 'next': next_step}
                ]}
            ]
        })
    # End lesson
    steps.append({
        'id': f'{topic_name}_end_lesson',
        'action': f'utter_{topic_name}_end',
        'next': 'END'
    })
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(flow, f, allow_unicode=True, sort_keys=False)
    print(f"Đã sinh file flow {output_file}")

def load_data_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    topic = data['topic']
    grammars = data['grammars']
    practices = data['practices']
    return topic, grammars, practices

if __name__ == "__main__":
    json_path = "scripts/input.json"
    topic, grammars, practices = load_data_from_json(json_path)
    generate_grammar_yml(topic, grammars, practices, f"{topic}_grammar_domain.yml")
    generate_grammar_flow_yml(topic, grammars, practices, f"{topic}_grammar_flow.yml") 