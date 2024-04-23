from typing import List, Mapping, Optional, Tuple

from transformers import AutoModelForSequenceClassification, AutoTokenizer


class ContentModerator:
    LABELS_ACRONYMS_MAPPING: Mapping[str, str] = {
        "S": "Sexual",
        "H": "Hate",
        "V": "Violence",
        "HR": "Harrassment",
        "SH": "Self-harm",
        "S3": "Sexual/minors",
        "H2": "Hate/threatening",
        "V2": "Violence/graphic",
        "OK": "Not offensive",
    }

    def __init__(self, model: Optional[str] = "./Text-Moderation"):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForSequenceClassification.from_pretrained(model)

    def infer(self, text: str) -> List[Tuple[str, float]]:
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        probabilities = logits.softmax(dim=-1).squeeze()
        labels = [
            self.model.config.id2label[idx] for idx in range(len(probabilities))
        ]
        label_prob_pairs = list(zip(labels, probabilities))
        label_prob_pairs.sort(key=lambda item: item[1], reverse=True)

        return list(
            map(
                lambda pair: (pair[0], float(pair[1])),
                label_prob_pairs,
            )
        )
