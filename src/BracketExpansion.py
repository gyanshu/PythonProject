# https://leetcode.com/discuss/interview-experience/5341224/Stripe-or-Backend-Engineer-or-Bangalore-or-Jun-2024-or-Reject



# with regex

import re

def bracket_expansion(expression):
    # Find the part enclosed in curly braces
    match = re.search(r"\{([^{}]+)}", expression)

    # If no valid brackets or single item, return input as-is
    if not match or ',' not in match.group(1):
        return [expression]

    prefix = expression[:match.start()]
    suffix = expression[match.end():]

    # Generate results by replacing the bracketed part with each token
    tokens = match.group(1).split(',')
    return [prefix + token + suffix for token in tokens]


# Test cases
inputs = [
    "/2022/{jan,feb,march}/report",
    "over{crowd,eager,bold,fond}ness",
    "read.txt{,.bak}",
    "sun{mars}rotation",
    "minimum{}change",
    "hello-world",
    "hello-{-world",
    "hello-}-weird-{-world"
]

for inp in inputs:
    print(f"Input: {inp}\nOutput: {bracket_expansion(inp)}\n")


# without regex

# def bracket_expansion(expression):
#     # Find the opening and closing braces
#     start_idx = expression.find("{")
#     end_idx = expression.find("}")
#
#     # Check if there's any mismatch in the braces
#     if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
#         return [expression]  # Invalid or malformed, return input as-is
#
#     # Extract prefix and suffix
#     prefix = expression[:start_idx]
#     suffix = expression[end_idx + 1:]
#
#     # Extract the content inside the braces
#     tokens = expression[start_idx + 1:end_idx].split(',')
#
#     # If there are fewer than 2 tokens inside the braces, return input as-is
#     if len(tokens) < 2:
#         return [expression]
#
#     # Generate the expanded expressions
#     return [prefix + token + suffix for token in tokens]
#
#
# # Test cases for both Part 1 and Part 2
# inputs = [
#     "/2022/{jan,feb,march}/report",  # Valid bracket expansion
#     "over{crowd,eager,bold,fond}ness",  # Valid bracket expansion
#     "read.txt{,.bak}",  # Valid bracket expansion
#     "sun{mars}rotation",  # Invalid - Only one token
#     "minimum{}change",  # Invalid - Empty braces
#     "hello-world",  # Invalid - No braces
#     "hello-{-world",  # Invalid - Malformed braces
#     "hello-}-weird-{-world",  # Invalid - Malformed braces
#     "hello-{a, b}-weird {gg, eg}--world" # not handled
# ]
#
# for inp in inputs:
#     result = bracket_expansion(inp)
#     print(f"Input: {inp}")
#     for r in result:
#         print(f"Output: {r}")
