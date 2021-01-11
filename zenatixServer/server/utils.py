def add_data(f, data, data_sheet_headers):
    raw_data = []
    for data_sheet_header in data_sheet_headers:
        raw_data.append(data[data_sheet_header])
    raw_data = ','.join(raw_data)
    raw_data += '\n'
    f.write(raw_data)