# https://leetcode.com/discuss/interview-experience/4905399/Stripe-Interview-Experience-%3A-No-Offer

# Part 1

def redact_card_numbers(text):
    tokens = text.split()

    for i, token in enumerate(tokens):
        # Check if token is a valid credit card number (13-16 digits)
        if token.isdigit() and 13 <= len(token) <= 16:
            # Redact the token, replacing all digits except the last 4 with 'x'
            tokens[i] = 'x' * (len(token) - 4) + token[-4:]

    return ' '.join(tokens)


# Example cases:
print(redact_card_numbers("1234567890123456 is a number"))  # "xxxxxxxxxxxx3456 is a number"
print(redact_card_numbers("basic_string 12345 no redaction"))  # "basic_string 12345 no redaction"
print(redact_card_numbers(
    "an embedded number 1234567890123456 in the string"))  # "an embedded number xxxxxxxxxxxx3456 in the string"

# Part 2

def redact_card_numbers(text):
    tokens = text.split()

    def is_valid_card(card_number):
        if len(card_number) == 13 or len(card_number) == 16:
            # Visa: starts with 4, length 13 or 16
            if card_number[0] == '4':
                return True
            # American Express: starts with 34 or 37, length 15
            elif len(card_number) == 15 and (card_number[:2] == '34' or card_number[:2] == '37'):
                return True
            # Mastercard: starts with 51-55 or 2221-2720, length 16
            elif len(card_number) == 16 and (
                    (51 <= int(card_number[:2]) <= 55) or (2221 <= int(card_number[:4]) <= 2720)
            ):
                return True
        return False

    for i, token in enumerate(tokens):
        # Check if token is a valid credit card number (13-16 digits)
        if token.isdigit() and 13 <= len(token) <= 16 and is_valid_card(token):
            # Redact the token, replacing all digits except the last 4 with 'x'
            tokens[i] = 'x' * (len(token) - 4) + token[-4:]

    return ' '.join(tokens)


# Example cases:
print(redact_card_numbers("basic_string 12345 no redaction"))  # "basic_string 12345 no redaction"
print(redact_card_numbers("1234567890123456 is not a card"))  # "1234567890123456 is not a card"
print(redact_card_numbers("4234567890123456 is a valid visa"))  # "xxxxxxxxxxxx3456 is a valid visa"
