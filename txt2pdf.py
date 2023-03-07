import sys
import pdfkit
import os

os.system("rm out.html")
config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")

template1 = '''<html>
<head>
<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: lightgray;
  }
  .header {
    background-color: #F5F5F5;
    padding: 10px;
    border: 1px solid #CCC;
    
  }
  .label {
    display: inline-block;
    width: 60px;
    font-size: 18px;
    font-weight: bold;
  }
  .url {
    color: #0066CC;
    text-decoration: none;
  }
  .repo {
    color: #606060;
    text-decoration: none;
  }
</style>
</head>
<body>
<center><h1>Report of Exposed URLs</h1></center><br>
'''

template2 = "</body></html>"

f = open("out.html", "a")
f.write(template1)
f.close()

def text2pdf(filename):
  f = open(filename, "r")
  contents = f.readlines()
  f.close()
  base_url, repo_url = contents[0].strip().split(",")
  f = open("out.html", "a")
  f.write(f'''

<div class="header">
  <span class="label">URL:</span> <span><a href="{base_url}" 
class="url">{base_url}</a></span>
  <br>
  <span class="label">Repo:</span> <span><a href="{repo_url}" 
class="repo">{repo_url}</a></span>
</div>
<br>
<table>
<tr><th>Exposed URLs</th><th>Severity</th></tr>
  ''')
  for i in range(1, len(contents)):
    url = contents[i].strip()
    if url.endswith(".env") or url.endswith(".pem"):
      severity = "High"
      color = "#FB4836"
    elif url.endswith(".json") or url.endswith(".conf") or url.endswith(".xml") or url.endswith(".gitignore"):
      severity = "Medium"
      #color = "#FFA500"
      color = "#FF8C00"
    else:
      severity = "Low"
      color = "#32CD32"

    f.write(f'<tr><td><a href="{url}" style="color: {color}; text-decoration: none;">{url}</a></td><td><center>{severity}</center></td></tr>')
  f.write("</table><br><br>")
  f.close()

############## main ###############

txtfile = sys.argv[1]
text2pdf(txtfile)
f = open("out.html", "a")
f.write(template2)
f.close()

pdfkit.from_file('out.html', 'output.pdf', configuration=config)