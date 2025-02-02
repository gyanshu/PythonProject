# https://leetcode.com/discuss/interview-experience/4742657/Stripe-Phone-screen

def parseacceptlanguage(header, supported_languages):
    # Split the Accept-Language header into individual language tags
    requested_languages = header.split(", ")

    # Create a list to store the matched languages
    matched_languages = []

    # Iterate over the requested languages and add them to the result if they are supported
    for lang in requested_languages:
        if lang in supported_languages:
            matched_languages.append(lang)

    return matched_languages


# Test cases:
print(parseacceptlanguage("en-US, fr-CA, fr-FR", {"fr-FR", "en-US"}))  # ["en-US", "fr-FR"]
print(parseacceptlanguage("fr-CA, fr-FR", {"en-US", "fr-FR"}))  # ["fr-FR"]
print(parseacceptlanguage("en-US", {"en-US", "fr-CA"}))  # ["en-US"]
