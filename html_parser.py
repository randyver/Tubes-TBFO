import re

def get_tokens(file_location: str) -> list[str]:
    tokens = []

    with open(file_location) as file:
        c = file.read(1)
        while c != '':
            # Ignore whitespaces.
            if str.isspace(c):
                c = file.read(1)
                continue
            
            # If not a whitespace, but not part of a tag.
            is_token_text = False
            while c != '<':
                is_token_text = True
                c = file.read(1)

            if is_token_text:
                tokens.append("TEXT")

            # Start processing the tag.
            tag = []
            while c != '>':
                tag.append(c)
                c = file.read(1)
            tag.append('>')

            # Check if a tag has attributes..
            html_tag = ''.join(tag)
            if '="' in html_tag:
                # clean_tag contains no attributes.
                clean_tag = []
                for character in tag:
                    if character != ' ':
                        clean_tag.append(character)
                    else:
                        break
                clean_tag.append('>')
                tokens.append(''.join(clean_tag))

                # Append all attributes of the tag 
                pattern = r'(\w+)\s*=\s*["\'](.*?)["\']'
                matches = re.findall(pattern, html_tag)
                for attribute, _ in matches:
                    tokens.append(attribute)

            else:
                tokens.append(''.join(tag))
            
            c = file.read(1)
    return tokens



tokens = get_tokens('test/1.html')
print(tokens)