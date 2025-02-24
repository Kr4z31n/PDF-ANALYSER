import re
import sys

def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        return None

def find_xref_offsets(pdf_data):
    return [int(match.group(1)) for match in re.finditer(rb'startxref\s+(\d+)', pdf_data)]

def parse_xref_table(pdf_data, xref_offset):
    xref_table = {}
    if xref_offset is not None:
        pdf_data = pdf_data[xref_offset:]
        matches = re.finditer(rb'(\d{10}) (\d{5}) ([nf])', pdf_data)
        obj_number = 0
        for match in matches:
            byte_offset, gen_number, flag = match.groups()
            byte_offset = int(byte_offset)
            obj_number += 1
            if flag == b'n':
                xref_table[obj_number] = byte_offset
    return xref_table

def find_objects(pdf_data):
    return re.findall(rb'(\d+) \d+ obj', pdf_data)

def check_encryption(pdf_data):
    return b'/Encrypt' in pdf_data

def validate_xref_mapping(pdf_data, xref_tables):
    correct_matches = []
    wrong_matches = []
    obj_numbers = find_objects(pdf_data)
    obj_set = set(int(num) for num in obj_numbers)

    for xref_table in xref_tables:
        for obj_num, offset in xref_table.items():
            obj_match = re.match(rb'(\d+)\s+\d+\s+obj', pdf_data[offset:offset+20])
            if obj_match:
                actual_obj_num = int(obj_match.group(1))
                if actual_obj_num == obj_num - 1 and obj_num - 1 in obj_set:
                    correct_matches.append((obj_num, offset))
                else:
                    wrong_matches.append((obj_num, offset, actual_obj_num))
            else:
                wrong_matches.append((obj_num, offset, None))

    return correct_matches, wrong_matches

def parse_header(pdf_data):
    return pdf_data.startswith(b'%PDF-')

def parse_objects(pdf_data):
    return re.findall(rb'\d+ \d+ obj(.*?)endobj', pdf_data, re.DOTALL)

def parse_xref(pdf_data):
    return re.search(rb'startxref\s+(\d+)', pdf_data)

def parse_trailer(pdf_data):
    return re.search(rb'trailer\s*<<.*?>>', pdf_data, re.DOTALL)

def check_malformed_numbers(pdf_data):
    return re.findall(rb'\d+\.\d+\.\d+', pdf_data)

def check_encoding(pdf_data):
    encodings = re.findall(rb'BT\s(.*?)\sET', pdf_data, re.DOTALL)
    for encoding in encodings:
        try:
            encoding.decode('utf-8')
        except:
            return False
    return True

def check_keywords(pdf_data):
    keywords = [b'obj', b'endobj', b'xref', b'trailer', b'startxref']
    for keyword in keywords:
        if pdf_data.find(keyword) == -1:
            return False
    return True

def check_integrity(pdf_data):
    if not parse_header(pdf_data):
        return "Corrupted - Invalid header"
    if not parse_objects(pdf_data):
        return "Corrupted - No objects found"
    if not parse_xref(pdf_data):
        return "Corrupted - No xref table found"
    if not parse_trailer(pdf_data):
        return "Corrupted - No trailer found"
    if check_malformed_numbers(pdf_data):
        return "Corrupted - Malformed numbers"
    if not check_encoding(pdf_data):
        return "Corrupted - Invalid character encoding"
    if not check_keywords(pdf_data):
        return "Corrupted - Missing essential keywords"
    return "Normal"

def analyze_pdf(file_path):
    pdf_data = read_pdf(file_path)
    if pdf_data is None:
        return None, "Error reading PDF file"

    if check_encryption(pdf_data):
        return None, "Encrypted"

    integrity_status = check_integrity(pdf_data)
    if integrity_status != "Normal":
        return None, integrity_status

    xref_offsets = find_xref_offsets(pdf_data)
    if not xref_offsets:
        return None, "XRef table not found"

    xref_tables = [parse_xref_table(pdf_data, offset) for offset in xref_offsets]
    correct_matches, wrong_matches = validate_xref_mapping(pdf_data, xref_tables)

    if wrong_matches:
        return "Corrupt", []
    elif correct_matches:
        return "Normal", []
    else:
        return "Corrupt", ["No valid objects found"]


if len(sys.argv) != 2:
    print("Usage: python3 script.py <pdf_file>")
    sys.exit(1)

file_path = sys.argv[1]
file_status, errors = analyze_pdf(file_path)
if errors:
    print(f"File Status: {errors}")
else:
    print(f"File Status: {file_status}")


