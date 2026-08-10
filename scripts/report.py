import json
from jinja2 import Template

qc_json_path = snakemake.input.qc_json
summary_json_path = snakemake.input.summary_json
output_html = snakemake.output.html

with open(qc_json_path) as f:
    qc_results = json.load(f)

with open(summary_json_path) as f:
    population_sumary = json.load(f)


html_template = Template("""
<!DOCTYPE html>
<html>
<head>
    <title>QC Report - {{ sample }}</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        .pass { color: green; font-weight: bold; }
        .fail { color: red; font-weight: bold; }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>QC & Population Report</h1>
    <h2>Sample: {{ sample }}</h2>

    <h3>QC Results</h3>
    <p>Overall: <span class="{{ 'pass' if qc.overall_pass else 'fail' }}">
        {{ 'PASS' if qc.overall_pass else 'FAIL' }}
    </span></p>
    <ul>
        <li>Event count: {{ qc.event_count }} ({{ 'OK' if qc.event_count_ok else 'FAIL' }})</li>
        <li>Channels present: {{ 'OK' if qc.channels_ok else 'FAIL - missing: ' + qc.missing_channels|join(', ') }}</li>
        <li>No constant channels: {{ 'OK' if qc.no_constant_channels else 'FAIL - constant: ' + qc.constant_channels|join(', ') }}</li>
    </ul>

    <h3>Population Breakdown</h3>
    <p>Total events: {{ summary.total_events }}</p>
    <table>
        <tr><th>Population</th><th>Count</th><th>Percentage</th></tr>
        {% for pop, pct in summary.population_percentages.items() %}
        <tr>
            <td>{{ pop }}</td>
            <td>{{ summary.population_counts[pop] }}</td>
            <td>{{ pct }}%</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
""")

rendered_html = html_template.render(
    sample = qc_results["sample"],
    qc = qc_results,
    summary = population_sumary
)

with open(output_html, "w") as f:
    f.write(rendered_html)