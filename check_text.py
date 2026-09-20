content = open('dse-wrap-2026-09-18.html', encoding='utf-8').read()
import re
text_only = re.sub(r'<[^>]+>', ' ', content)
text_only = re.sub(r'\s+', ' ', text_only)

start_idx = text_only.find('Turnover Cools')
end_idx = text_only.find('reach that day') + 20

print(text_only[start_idx:end_idx])
