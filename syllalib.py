import parquet
import re
from collections import Counter

def load_names_from_parquet(file_path):
    """Load unique names from parquet file and return as list."""
    just_names = []
    with open(file_path, "rb") as fo:
        for row in parquet.reader(fo):
            p = row[0]
            if p not in just_names:
                just_names.append(p)
    return just_names
            

def count_syllables(word):
    """Count syllables in a word."""
    word = word.lower()
    
    if not word:
        return 0
    
    # Handle diphthongs
    diphthongs = ['ai', 'ay', 'ei', 'ey', 'oi', 'oy', 'ui', 'au', 'eau', 'eu', 'ou']
    for diph in diphthongs:
        word = word.replace(diph, 'X')
    
    # Remove final silent e
    if word.endswith('e') and len(word) > 1:
        word = word[:-1]
    
    # Count vowel groups
    vowels = "aeiouyàâäéèêëîïôöùûüÿæœx"
    count = 0
    prev_is_vowel = False
    
    for char in word:
        is_vowel = char.lower() in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    
    # Ensure at least one syllable
    return max(1, count)

def get_syllable_positions(name):
    """Identify syllable boundaries in a name."""
    name = name.lower()
    vowels = "aeiouyàâäéèêëîïôöùûüÿæœ"
    consonants = "bcdfghjklmnpqrstvwxzç"
    positions = [0]  # Start of name
    
    # Handle special sequences
    diphthongs = ['ai', 'ay', 'ei', 'ey', 'oi', 'oy', 'ui', 'au', 'eau', 'eu', 'ou']
    
    i = 1
    while i < len(name) - 1:
        # Skip diphthongs
        skip = False
        for diph in diphthongs:
            if i < len(name) - len(diph) + 1:
                if name[i:i+len(diph)] == diph:
                    skip = True
                    break
        
        if skip:
            i += 1
            continue
        
        # Vowel followed by consonant-vowel
        if (name[i-1] in vowels and 
            name[i] in consonants and 
            i+1 < len(name) and name[i+1] in vowels):
            positions.append(i)
        
        # Two consonants between vowels
        if (i+2 < len(name) and
            name[i-1] in vowels and 
            name[i] in consonants and 
            name[i+1] in consonants and
            name[i+2] in vowels):
            positions.append(i+1)
        
        # After vowel-vowel sequence
        if (name[i-1] in vowels and name[i] in vowels):
            positions.append(i)
        
        i += 1
    
    return positions

def split_name_at_syllables(name):
    """Split a name into prefix and suffix along syllable boundaries."""
    # Handle multi-word names
    parts = re.split(r'[\s\-\']', name)
    parts = [p for p in parts if p]
    
    if len(parts) > 1:
        # For multi-part names, split at the middle part
        middle_index = len(parts) // 2
        prefix = ' '.join(parts[:middle_index])
        suffix = ' '.join(parts[middle_index:])
    else:
        # For single-word names, split by syllables
        word = parts[0]
        syllable_count = count_syllables(word)
        
        if syllable_count == 1:
            # Single syllable: whole word as prefix
            prefix = word
            suffix = ""
        else:
            # Get syllable boundaries
            positions = get_syllable_positions(word)
            
            if positions and len(positions) > 1:
                # Split near the middle syllable
                middle_idx = len(positions) // 2
                split_point = positions[middle_idx]
                prefix = word[:split_point]
                suffix = word[split_point:]
            else:
                # Fallback: split at middle of the word
                split_point = len(word) // 2
                prefix = word[:split_point]
                suffix = word[split_point:]
    
    return prefix, suffix

def get_name_arrays(file_path):
    """Load parquet file and return arrays of name prefixes and suffixes."""
    # Load names
    names = load_names_from_parquet(file_path)
    
    # Split names into prefixes and suffixes
    prefixes = []
    suffixes = []
    
    for name in names:
        if not isinstance(name, str) or not name.strip():
            continue
            
        prefix, suffix = split_name_at_syllables(name)
        prefixes.append(prefix)
        suffixes.append(suffix)
    
    return names, prefixes, suffixes

if __name__ == "__main__":
    file_path = "01_04_prenom.parquet"
    names, prefixes, suffixes = get_name_arrays(file_path)
    
    print(f"Loaded {len(names)} names")
    print(f"Created {len(prefixes)} prefixes and {len(suffixes)} suffixes")
    
    # Print some examples
    for i in range(min(5, len(names))):
        print(f"{names[i]} -> '{prefixes[i]}' + '{suffixes[i]}'")