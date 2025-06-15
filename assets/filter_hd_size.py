import json

# Đường dẫn file
file_path = 'assets/gif_data.json'

# Đọc dữ liệu gốc
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Hàm lọc file.hd
def filter_hd_file(entry):
    if isinstance(entry, dict):
        new_entry = {}
        for k, v in entry.items():
            if k == 'file' and isinstance(v, dict):
                # Chỉ giữ lại trường 'hd' trong 'file'
                if 'hd' in v:
                    new_entry['file'] = {'hd': v['hd']}
            else:
                new_entry[k] = filter_hd_file(v)
        return new_entry
    elif isinstance(entry, list):
        return [filter_hd_file(item) for item in entry]
    else:
        return entry

# Lọc dữ liệu
filtered_data = filter_hd_file(data)

# Ghi đè lại file
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print('Đã lọc xong, chỉ giữ lại file.hd.') 