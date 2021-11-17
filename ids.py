from serp.env import MAX_FILENAME_LEN

def title2file(string):
    """Makes a filename from a publication title by replacing special
    characters with escape codes."""

    for replacee, replacement in (('-', '.dash.'),
                                  (', ', ','),  # commas are allowed
                                  (' ', '-'),
                                  ('/', '.fslash.'),
                                  ('(', '.lparan.'),
                                  (')', '.rparan.'),
                                  ('?', '.qmark.'),
                                  ('*', '.star.')):
        string = string.replace(replacee, replacement)

    return string[:MAX_FILENAME_LEN]

def hash_dict(dct):
    slist = sorted(key + str(dct[key]) for key  in dct)
    return title2file(''.join(slist))[:MAX_FILENAME_LEN]
