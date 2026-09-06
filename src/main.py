import re
import json
import os

def read_input(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
               return file.read()
        
def email_hunt(text_content):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text_content)
    alu_official_email = []
    alu_alumni_email = []
    alu_si_email = []
    other_email = []
    for email in set(emails):
        if email.endswith("@alueducation.com"):
                          alu_official_email.append(email)
        elif email.endswith("@alumni.alueducation.com"):
                alu_alumni_email.append(email)
        elif email.endswith("@si.alueducation.com"):
                alu_si_email.append(email)
        else:
                other_email.append(email)
    return {
        "alu_official_email": alu_official_email,
        "alu_alumni_email": alu_alumni_email,
        "alu_si_email": alu_si_email,
        "other_email": other_email,
    }

def card_2face(text_content):
        card_pattern =r"\b(?:\d[ -]*?){13,19}\b"
        og_card = re.findall(card_pattern, text_content)

        masked_card = []
        for card in og_card:
                digits_only = re.sub(r"\D", "", card)
                if 13 <= len(digits_only) <= 19:
                        last_four = digits_only[-4:]
                        hidden_card = f"**** **** **** {last_four}"

                        if hidden_card not in masked_card:
                                masked_card.append(hidden_card)

        return masked_card
def call_log(text_content):
        phone_pattern = (
                r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
        )

        phones = re.findall(phone_pattern, text_content)
        return list(set(phones))
def link_hunter(text_content):
        url_pattern = r"https?://[^\s/$.?#].[^\s]*"
        urls = re.findall(url_pattern, text_content)
        clean_urls = [re.sub(r"[.,;)]$", "", url) for url in urls]
        return list(set(clean_urls))
def cleaned_text(raw_text):
        clean_text = re.sub(r'<[^>]*>', '', raw_text)
        return clean_text
if __name__ == "__main__":
     
    word = read_input("input/raw-text.txt")
    clean_word = cleaned_text(word)
    print("The file was successfully loaded :)")
    print(f"character count: {len(clean_word)}")

    found_data = email_hunt(clean_word)
    print("\nEmail hunt successful ^.^ !!")
    print(found_data)

    card_data = card_2face(clean_word)
    print("\nCard 2face successful  ^.^ !")
    print(card_data)

    phone_data = call_log(clean_word)
    print("\nCall log successful  ^.^ !")
    print(phone_data)

    link_data = link_hunter(clean_word)
    print("\nLink hunter successful  ^.^ !")
    print(link_data)

    summary = {
            "emails": found_data,
            "masked_cards": card_data,
            "phone_numbers": phone_data,
            "urls": link_data,
    }
    os.makedirs("output", exist_ok=True)
    output_file_path = os.path.join("output", "sample-output.json")

    with open(output_file_path, "w", encoding="utf-8") as file:
            json.dump(summary, file, indent=4)

    print(
            "\n Extractions done ^.^! saved to output/sample-output.json ^.^ !!"
            )

