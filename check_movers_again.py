content = open('dse-wrap-2026-09-18.html', encoding='utf-8').read()
import re
text_only = re.sub(r'<[^>]+>', ' ', content)
text_only = re.sub(r'\s+', ' ', text_only)
start_idx = text_only.find('AFRIPRISE 740')
end_idx = text_only.find('AFRIPRISE was the standout')
print(text_only[start_idx:end_idx])
