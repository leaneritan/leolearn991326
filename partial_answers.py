import json

def generate_answers(blanks_path):
    with open(blanks_path, 'r') as f:
        blanks = json.load(f)

    # We will manually (with AI help) fill these.
    # I will output the structure and then fill it.

    answers = {}
    for b in blanks:
        # I'll provide the logic for common patterns
        text = b['text'].lower()
        ans = ""

        # Page 21: C or P
        if b['page'] == 21 and '_______' in b['text']:
            if 'white house' in text: ans = "P"
            elif 'green dress' in text: ans = "C"
            elif 'tall building' in text: ans = "C"
            elif 'empire state building' in text: ans = "P"
            elif 'yellow river' in text: ans = "P"
            elif 'muddy river' in text: ans = "C"
            elif 'the governor' in text and 'parker' not in text: ans = "C"
            elif 'governor parker' in text: ans = "P"
            elif 'oregon trail' in text: ans = "P"
            elif 'winding trail' in text: ans = "C"

        # Page 51: Pronouns
        elif b['page'] == 51:
            if '1 ' in text and 'peter and i' in text: ans = "We"
            elif '2 ' in text and 'sue' in text: ans = "her"
            elif '3 ' in text and 'my brother' in text: ans = "He"
            elif '4 ' in text and 'students like' in text: ans = "him"
            elif '5 ' in text and 'children' in text: ans = "you"
            elif '6 ' in text and 'people' in text: ans = "they"
            elif '7 ' in text and 'mom' in text: ans = "She"
            elif '8 ' in text and 'sky' in text: ans = "It"
            elif '9 ' in text and 'waiting for' in text:
                if 'waiting for' in text and b['blank_index'] == 0: ans = "you"
                if 'with' in text and b['blank_index'] == 0: ans = "us"
            elif 'with' in text: ans = "us"
            elif '10 ' in text: ans = "I"
            elif '11 ' in text:
                if 'return' in text and b['blank_index'] == 0: ans = "it"
                else: ans = "me"
            elif '12 ' in text: ans = "you"

        # Page 52: Reflexive Pronouns
        elif b['page'] == 52 and b['y'] < 60:
            if 'help us' in text: ans = "ourselves"
            elif 'jane' in text: ans = "herself"
            elif 'they' in text: ans = "themselves"
            elif 'i hurt' in text: ans = "myself"
            elif 'john' in text: ans = "yourself"
            elif 'children' in text: ans = "yourselves"
            elif 'tom' in text: ans = "himself"
            elif 'dog' in text: ans = "itself"

        # Page 52: Interrogative Pronouns
        elif b['page'] == 52 and b['y'] >= 60:
            if 'matter' in text: ans = "What"
            elif 'invented' in text: ans = "Who"
            elif 'twins' in text: ans = "Which"
            elif 'wish to speak' in text: ans = "Whom"
            elif 'car in front' in text: ans = "Whose"
            elif 'knows the answer' in text: ans = "Who"
            elif 'chicken or the egg' in text: ans = "Which"
            elif 'like to drink' in text: ans = "What"
            elif 'win the race' in text: ans = "Which"
            elif 'stamp collector' in text: ans = "What"

        # Page 88: am, is, are
        elif b['page'] == 88:
            if b['y'] < 50:
                if 'they' in text: ans = "are"
                elif 'he' in text: ans = "is"
                elif 'you taller' in text: ans = "are"
                elif 'she' in text: ans = "is"
                elif 'we' in text: ans = "are"
                elif 'it' in text: ans = "is"
                elif 'i' in text: ans = "am"
                elif 'you all' in text: ans = "are"
            else:
                if 'dog' in text: ans = "is"
                elif 'robert' in text: ans = "is"
                elif 'flowers' in text: ans = "are"
                elif 'schools' in text: ans = "are"
                elif 'math' in text: ans = "is"
                elif 'dinner ready' in text: ans = "is"
                elif 'computer' in text: ans = "is"
                elif 'windows' in text: ans = "are"
                elif 'sue and jane' in text: ans = "are"
                elif 'hair' in text: ans = "is"

        # Default for those I haven't coded yet
        if ans:
            answers[b['key']] = ans

    return answers

if __name__ == "__main__":
    # This is just a partial generator to demonstrate.
    # I will actually provide a full answers.json by processing more.
    pass
