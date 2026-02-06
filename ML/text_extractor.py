import re

SYMPTOMS = {
    "diarrhea": [
        "diarrhea", "loose motion", "loose motions", "loosemotion", "stool"
    ],
    "vomiting": [
        "vomiting", "vomit", "throw up", "throws up"
    ],
    "fever": [
        "fever", "high temperature", "temperature"
    ]
}

SOURCES = ["pond", "river", "handpump", "tap", "well"]

NEGATION_PATTERNS = [
    r"no\s+{}",
    r"not\s+{}",
    r"doesn'?t.*{}",
    r"without\s+{}",
    r"never\s+{}",
    r"doesn'?t\s+have\s+{}",
    r"doesn'?t\s+present\s+any\s+{}"
]


def _has_negation(text, word):
    for pat in NEGATION_PATTERNS:
        p = pat.format(re.escape(word))
        if re.search(p, text):
            return True
    return False


def _extract_number_before(text, keyword):
    """
    finds a number before a keyword within a small window
    e.g. '3 people had diarrhea'
    """
    pattern = r"(\d+)\s+(?:people|persons|children|cases)?\s*(?:have|had|with)?\s*" + re.escape(keyword)
    m = re.search(pattern, text)
    if m:
        return int(m.group(1))
    return None


def extract_from_text(report_text):

    text = report_text.lower()

    result = {
        "diarrhea": 0,
        "vomiting": 0,
        "fever": 0,
        "suspected_source": None
    }


    for symptom, keywords in SYMPTOMS.items():

        found = False
        value = 0

        for kw in keywords:

            if kw in text:

                # check negation
                if _has_negation(text, kw):
                    found = True
                    value = 0
                    break

                # try to extract number
                num = _extract_number_before(text, kw)

                if num is not None:
                    found = True
                    value = num
                    break
                else:
                    # keyword present, no number, no negation
                    found = True
                    value = 1
                    break

        if found:
            result[symptom] = value


    for src in SOURCES:
        if src in text:
            result["suspected_source"] = src
            break

    return result


# small test
if __name__ == "__main__":

    tests = [
        "Today 3 people have loose motions and 2 are vomiting after using pond water.",
        "this house is very sick and the person doesnt present any vomiting but has fever",
        "No diarrhea and no vomiting but 2 persons have fever after using river water"
    ]

    for t in tests:
        print(t)
        print(extract_from_text(t))
        print()
