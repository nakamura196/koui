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

import difflib
import bs4

def convert(name_1, text_1, name_2, text_2):
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

    return str(soup)