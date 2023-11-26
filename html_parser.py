import re

def parse_no_attributes(file_location: str) -> list[str]:
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
                # pattern = r'(\w+)\s*=\s*["\'](.*?)["\']'
                # matches = re.findall(pattern, html_tag)
                # for attribute, _ in matches:
                #     tokens.append(attribute)

            else:
                tokens.append(''.join(tag))
            
            c = file.read(1)
    new_tokens = []
    for i in tokens:
        if i[:4] != "<!--":
            new_tokens.append(i)
    tokens = new_tokens
    return tokens


def parse_attributes(file_location: str) -> list[str]:
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

            # if is_token_text:
            #     tokens.append("TEXT")

            # Start processing the tag.
            tag = []
            while c != '>':
                tag.append(c)
                c = file.read(1)
            tag.append('>')

            tag_string = ''.join(tag)

            if tag[1] == '/':
                c = file.read(1)
                continue

            if '="' in tag_string:
                # clean_tag contains no attributes.
                clean_tag = []
                for character in tag:
                    if character != ' ':
                        clean_tag.append(character)
                    else:
                        break
                clean_tag.append('>')
                tokens.append(''.join(clean_tag))

                attributes = dict(re.findall(r'(\S+)=["\']?((?:.(?!["\']?\s+(?:\S+)=|[>"\']))+.)["\']?', tag_string))
                for attribute, value in attributes.items():
                    tokens.append(attribute)
                    if attribute == 'id':
                        tokens.append('ID_VAL')

                    elif attribute == "class":
                        tokens.append('CLASS_VAL')
                    
                    elif attribute == 'style':
                        tokens.append("STYLE_VAL")
                    
                    elif attribute == "alt":
                        tokens.append("ALT_VAL")
                    
                    elif attribute == 'href':
                        tokens.append("HREF_VAL")
                    
                    elif attribute == "action":
                        tokens.append("ACTION_VAL")
                    


                    elif attribute == 'rel':
                        tokens.append('REL_VAL')
                    elif attribute == 'src':
                        tokens.append("SRC_VAL")
                    elif attribute == "type":
                        tokens.append(value.replace(' ', ''))
                    elif attribute == "method":
                        tokens.append(value.replace(' ', ''))

            else:
                tokens.append(tag_string)

            tokens.append("INIT")
            c = file.read(1)
    new_tokens = []
    for i in tokens:
        if i[:4] != "<!--":
            new_tokens.append(i)
    tokens = new_tokens
    return tokens



# tokens = parse_attributes('test/1.html')
# print(tokens)