from lxml import html
import requests
page = requests.get('http://global-health-impact.org/organization.php')
tree = html.fromstring(page.content)