from serp.env import MAX_FILENAME_LEN, ORDERED_KEYS

def title2file(string):
    """Makes a filename from a publication title by replacing special
    characters with escape codes."""

    for replacee, replacer in (('-', '.dash.'),
                                  (', ', ','),  # commas are allowed
                                  (' ', '-'),
                                  ('/', '.fslash.'),
                                  ('(', '.lparan.'),
                                  (')', '.rparan.'),
                                  ('?', '.qmark.'),
                                  ('*', '.star.')):
        string = string.replace(replacee, replacer)

    return string[:MAX_FILENAME_LEN]

def hash_dict(dct):
    string = ''
    for key in ORDERED_KEYS:
        try:
            string += str(dct[key])
        except KeyError:
            pass

    return title2file(string)[:MAX_FILENAME_LEN]
