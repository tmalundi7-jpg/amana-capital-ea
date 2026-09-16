import re

with open('templates/current_prices_template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the table have 7 columns
new_html = '''<!-- PRICES_TABLE_START -->
<table class="data-table gold-grid-table">
    <thead>
        <tr>
            <th>Ticker</th>
            <th>Company</th>
            <th>Sector</th>
            <th>Last Price (TZS)</th>
            <th>Change (%)</th>
            <th>Volume</th>
            <th>Turnover (TZS)</th>
        </tr>
    </thead>
    <tbody>
        {% for eq in data.equities %}
        <tr>
            <td><strong>{{ eq.ticker }}</strong></td>
            <td>{{ eq.company | default('') }}</td>
            <td>{{ eq.sector | default('') }}</td>
            <td><strong>{{ "{:,.0f}".format(eq.close) }}</strong></td>
            <td class="{% if eq.change_pct > 0 %}change-positive{% elif eq.change_pct < 0 %}change-negative{% endif %}">
                <strong>{% if eq.change_pct > 0 %}+{{ "%.1f"|format(eq.change_pct) }}%{% elif eq.change_pct < 0 %}{{ "%.1f"|format(eq.change_pct) }}%{% else %}0.0%{% endif %}</strong>
            </td>
            <td>{{ eq.volume }}</td>
            <td>{{ eq.turnover | default('') }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
<!-- PRICES_TABLE_END -->'''

# Replace the first part of the template before the <script> tags
html = re.sub(r'<!-- PRICES_TABLE_START -->.*?<!-- PRICES_TABLE_END -->', new_html, html, flags=re.DOTALL)

with open('templates/current_prices_template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated template')
