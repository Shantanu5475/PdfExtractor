import pandas as pd

def detect_tables(page):
    tables = page.extract_tables()
    result = []

    if tables:
        for table in tables:
            header = table[0]
            data_rows = table[1:]
            df = pd.DataFrame(data_rows, columns=header)

            # Extract left-side words as car names
            words = page.extract_words()
            name_rows = group_left_column_words(words, len(data_rows))

            df.insert(0, "Car Name", name_rows)
            result.append(df)
    else:
        # fallback for borderless
        words = page.extract_words(use_text_flow=True)
        lines = group_words_to_rows(words)
        if lines:
            df = pd.DataFrame(lines)
            result.append(df)

    return result

def group_left_column_words(words, num_rows, x_threshold=100):
    """
    Extract car names (first column) from left-aligned text.
    This works by grouping words that appear close together vertically.
    """
    left_words = [w for w in words if w['x0'] < x_threshold]
    left_words.sort(key=lambda w: w['top'])

    # Cluster words into rows by vertical proximity
    rows = []
    current_row = []
    last_top = None
    threshold = 5  # adjust if too strict/loose

    for word in left_words:
        if last_top is None or abs(word['top'] - last_top) <= threshold:
            current_row.append(word)
        else:
            rows.append(" ".join([w['text'] for w in current_row]))
            current_row = [word]
        last_top = word['top']

    if current_row:
        rows.append(" ".join([w['text'] for w in current_row]))

    # Ensure we return a list of size equal to table rows
    while len(rows) < num_rows:
        rows.append("")
    return rows[:num_rows]
