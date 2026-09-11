import re
import json
import os
# reads content of input file
def read_input(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
#function that finds email addressed and categorizes them accoeding to si, alumni and official alu email address categories
def email_hunt(text_content):
    email_pattern = r'[\w.+-]+@[\w.-]+\.\w{2,}'
    emails = re.findall(email_pattern, text_content)
    alu_official_email = [] #create lists for the differnt email categories
    alu_alumni_email = []
    alu_si_email = []
    other_email = []

    # checks emails and puts them in right category depending on domain
    for email in set(emails):
          if email.endswith("@alumni.alueducation.com"):
                alu_alumni_email.append(email)
          elif email.endswith("@si.alueducation.com"):
                alu_si_email.append(email)
          elif email.endswith("@alueducation.com"):
                alu_official_email.append(email)
          else:
                other_email.append(email)
    return {
           "alu_official_email":alu_official_email,
           "alu_alumni_email":alu_alumni_email,
           "alu_si_email":alu_si_email,
           "other_email":other_email,
           
    }
def card_2face(text_content):   # function to find cc numbers and masks them for user privacy
       card_pattern = r"\b(?:\d[ -]*?){13,19}\b"
       og_card = re.findall(card_pattern, text_content)

       masked_card = []
# here removes spaces and dashes from the cc numbers
       for card in og_card:
              digits_only = re.sub(r"\D", "", card)
              if 13 <= len(digits_only) <= 19:
                  masked_card.append(digits_only)
       # removes duplicate cc numbers
       unique_digits = []
       for card in masked_card:
             if card not in unique_digits:
                   unique_digits.append(card)
          #the return value to show only last 4 digits of the cc number
       return [f"**** **** **** {digits[-4:]}" for digits in unique_digits]
#functionn to find phone numbers
def call_log(text_content):
       phone_pattern = (r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
       phones = re.findall(phone_pattern, text_content)
       #removes duplicate phone nos
       unique_phones = []
       for phone in phones:
             if phone not in unique_phones:
                   unique_phones.append(phone)

       return unique_phones
#function to find urls but in the code its links
def link_hunter(text_content):
       link_pattern = r"https?://\S+"
       links = re.findall(link_pattern, text_content)
       #removes any other punctuation that may be attached to link due to typing error e.tc,
       clean_links = [re.sub(r"[.,;)]+$", "", link) for link in links]
       #similar part of the functions to remove duplicate entries
       unique_links = []
       for link in clean_links:
             if link not in unique_links:
                   unique_links.append(link)
       return unique_links
#gets rid of html tags
def cleaned_text(raw_text):
       clean_text = re.sub(r'<[^>]*>', '', raw_text)
       return clean_text

if __name__ == "__main__":
       #reads input file and cleans it
       word = read_input("input/raw-text.txt")

       clean_word = cleaned_text(word)
       print("The file was successfully loaded :)")
       print(f"character count: {len(clean_word)}")
#extracts email addresses
       found_data = email_hunt(clean_word)
       print(found_data)
#extract cc numbers
       card_data = card_2face(clean_word)
       print("\nCards extracted successfully ^.^ !")
       print(card_data)
#extract phone numbers
       phone_data = call_log(clean_word)
       print("\nCall log successful ^.^ !")
       print(phone_data)
#extracts links
       link_data = link_hunter(clean_word)
       print("\nLinks hunted successfull ^.^ !")
       print(link_data)
# summarises extarcted info into a dictionary
       summary = {
              "emails": found_data,
              "masked_cards": card_data,
              "phone_numbers": phone_data,
              "links": link_data,
       }    
       #creates output folder just in case it doesnt exist 
       os.makedirs("output", exist_ok=True)
       output_file_path = os.path.join("output", "sample-output.json")
#extarcted info is then saved as a JSON file
       with open(output_file_path, "w", encoding="utf-8") as file:
              json.dump(summary, file, indent=4)
              print(
                     "\n Extractions done ^.^! saved to output/sample-output.json ^.^ !!"
              )