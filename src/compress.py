def compress(word: str) -> str:
    """Compress a word by keeping the first and last character and replacing the middle with its count."""
    if len(word) <= 2:
        return word
    return f"{word[0]}{len(word) - 2}{word[-1]}"


def merge(compressed1: str, compressed2: str) -> str:
    """Merge two compressed parts into a single compressed form."""
    num1, num2 = int(compressed1[1:-1]), int(compressed2[1:-1])
    merged_length = num1 + num2 + 2
    return f"{compressed1[0]}{merged_length}{compressed2[-1]}"


def process_minor_parts(segment: str, threshold: int) -> list[str]:
    """Process minor parts of a segment while respecting the threshold."""
    minor_parts = [compress(part) for part in segment.split(".")]
    while len(minor_parts) > threshold:
        minor_parts[-2] = merge(minor_parts[-2], minor_parts[-1])
        minor_parts.pop()
    return minor_parts


def compress_url(url: str, threshold: int) -> str:
    """Compress a URL while maintaining major and minor part constraints."""
    if not isinstance(url, str) or not isinstance(threshold, int) or threshold < 1:
        raise ValueError("URL must be a string and threshold must be a positive integer.")

    major_parts = []
    for segment in url.split("/"):
        minor_parts = process_minor_parts(segment, threshold)
        major_parts.append(".".join(minor_parts))

    return "/".join(major_parts)


def run_examples():
    """Execute test cases and display results."""
    test_cases = [
        ("stripe.com/payments/checkout/customer.john.doe", 2),
        ("www.api.stripe.com/checkout", 3)
    ]

    for original, threshold in test_cases:
        print(f"Original: {original}")
        print(f"Compressed: {compress_url(original, threshold)}")
        print("-")


if __name__ == "__main__":
    run_examples()
