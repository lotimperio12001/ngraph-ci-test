from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('scoreboard', 'templates'),
    autoescape=select_autoescape(['html'])
)

template_base = env.get_template('base.html')
static_base = template_base.render(the='variables', go='here')

with open("static_page/static_base.html", "w") as f:
    f.write(static_base)

template_charts = env.get_template('index.html')
ar = "[10, 2, 3]"
static_charts = template_charts.render(values=ar)

with open("static_page/static_charts.html", "w") as f:
    f.write(static_charts)
