template = '''<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://raw.githubusercontent.com/ldasjp8/tei-example/main/tei_all.rng" schematypens="http://relaxng.org/ns/structure/1.0" type="application/xml"?>

<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title>Title</title>
            </titleStmt>
            <publicationStmt>
                <p>Publication</p>
            </publicationStmt>
            <sourceDesc>
                <listWit></listWit>
            </sourceDesc>
        </fileDesc>
    </teiHeader>
    <text>
        <body>
        </body>
    </text>
</TEI>'''

html_template = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <!-- Bootstrap CSS -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
      crossorigin="anonymous"
    />

    <title>校異情報</title>
    <style>
      .c0 {
        background-color: #ef9a9a;
      }
      .c1 {
        background-color: #f48fb1;
      }
      .c2 {
        background-color: #ce93d8;
      }
      .c3 {
        background-color: #b39ddb;
      }
      .c4 {
        background-color: #9fa8da;
      }
      .c5 {
        background-color: #90caf9;
      }
      .c6 {
        background-color: #81d4fa;
      }
      .c7 {
        background-color: #80deea;
      }
      .c8 {
        background-color: #80cbc4;
      }
      .c9 {
        background-color: #a5d6a7;
      }
      .c10 {
        background-color: #c5e1a5;
      }
      .c11 {
        background-color: #e6ee9c;
      }
      .c12 {
        background-color: #fff59d;
      }
      .c13 {
        background-color: #ffe082;
      }
      .c14 {
        background-color: #ffcc80;
      }
      .c15 {
        background-color: #ffab91;
      }
      .c16 {
        background-color: #bcaaa4;
      }
      .c17 {
        background-color: #b0bec5;
      }
      .c18 {
        background-color: #eeeeee;
      }
    </style>
  </head>
  <body>
    <div class="container-fluid">
      <div class="row">
        <div class="col" id="a" style="height: 600px; overflow: auto; padding-bottom: 600px;"></div>

        <div class="col" id="b" style="height: 600px; overflow: auto; padding-bottom: 600px;"></div>
      </div>
    </div>

    <script
      type="text/javascript"
      src="https://code.jquery.com/jquery-3.4.1.min.js"
    ></script>

    <script>
      $(document).ready(function () {
        $("span").on("click", function () {
          const id = $(this).attr("id")
          const ab = id.substring(0,1)
          const index = id.substring(1)
          $("#a").scrollTop($('#a').scrollTop() + $('#a' + index).offset().top)
          $("#b").scrollTop($('#b').scrollTop() + $('#b' + index).offset().top)
        });
      });
    </script>
  </body>
</html>
'''

import difflib
import bs4

def export_xml(configs):
    soup = bs4.BeautifulSoup(template, 'xml')

    listWit = soup.find("listWit")
    for i in range(len(configs)):
        config = configs[i]
        witness = soup.new_tag("witness")
        listWit.append(witness)
        witness["xml:id"] = "t{}".format(i+1)
        witness.append(config["name"])

    text = configs[0]["text"]

    diffs = configs[0]["diffs"]

    for j in range(len(diffs)):
        index = len(diffs) - j - 1
        a_diff = diffs[index]
        b_diff = configs[1]["diffs"][index]

        a_start = a_diff["start"]
        a_size = a_diff["size"]

        a_text = configs[0]["text"][a_start:a_start+a_size]
        b_text = configs[1]["text"][b_diff["start"]:b_diff["start"]+b_diff["size"]]
        app = soup.new_tag("app")
        app["xml:id"] = "a{}".format(index+1)

        lem = soup.new_tag("lem")
        app.append(lem)
        lem.append(a_text)
        lem["wit"] = "#t1"
        
        rdg = soup.new_tag("rdg")
        app.append(rdg)
        rdg.append(b_text)
        rdg["wit"] = "#t2"

        text = text[:a_start] + str(app) + text[a_start+a_size:]

    text = text.replace("\n", "<lb/>")

    e = bs4.BeautifulSoup("<p>{}</p>".format(text), "xml")

    soup.find("body").append(e)

    return soup

def export_html(configs):
    soup = bs4.BeautifulSoup(html_template, 'html.parser')

    m = 19

    for i in range(len(configs)):
        config = configs[i]
        diffs = config["diffs"]

        text = config["text"]

        name = "a" if i == 0 else "b"
        
        for j in range(len(diffs)):

            index = len(diffs) - j - 1
            diff = diffs[index]

            start = diff["start"]
            size = diff["size"]
           
            mod = index % m

            text = text[:start] + "<span class='c{}' id='{}{}'>".format(mod, name, index) + text[start:start+size] + "</span>" + text[start+size:]

        text = text.replace("\n", "<br/>")
        
        # 名前をh2タグで追加
        text = "<h2>{}</h2>{}".format(config["name"], text)

        bs = bs4.BeautifulSoup(text, 'html.parser')
        soup.find(id=name).append(bs)

    return soup

def convert(name_1, text_1, name_2, text_2, output="html"):
    configs = [
        {
            "name": name_1,
            "text": text_1
        },
        {
            "name": name_2,
            "text": text_2
        }
    ]

    matcher = difflib.SequenceMatcher(lambda x: x in " \n", a=configs[0]["text"], b=configs[1]["text"], autojunk=False)
    blocks = matcher.get_matching_blocks()

    for config in configs:
        config["sames"] = []
        config["diffs"] = []

    for i in range(len(blocks)):
        match = blocks[i]

        configs[0]["sames"].append({"start": match.a, "size": match.size})
        configs[1]["sames"].append({"start": match.b, "size": match.size})

    for i in range(len(configs[0]["sames"]) - 1):

        for index in range(len(configs)):
            same = configs[index]["sames"][i]
            next_same = configs[index]["sames"][i + 1]

            configs[index]["diffs"].append({
                "start": same["start"] + same["size"],
                "size": next_same["start"] - (same["start"] + same["size"])
            })

    if output == "xml":
        return export_xml(configs)
    else:
        return export_html(configs)

    