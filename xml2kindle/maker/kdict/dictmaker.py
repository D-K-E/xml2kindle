# kindle dict maker which conforms to kindle publishing guidelines
# Author: Kaan Eraslan
# License: see, LICENSE

from lxml import etree
from typing import List, Dict
import pdb

from xml2kindle.maker.kdict.entrymaker import mkEntry


def mkMetaTag():
    "make meta tag"
    # <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    mtag = etree.Element("meta")
    mtag.set("http-equiv", "Content-Type")
    mtag.set("content", "text/html; charset=utf-8")
    return mtag


def mkHeadTag():
    return etree.Element("head")


def mkKdictTemplate() -> etree.Element:
    "make kindle dictionary template to be filled by entries"
    aguide = "https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
    nsmap: Dict[str, str] = {
        "math": "http://exslt.org/math",
        "svg": "http://www.w3.org/2000/svg",
        "saxon": "http://saxon.sf.net/",
        "xs": "http://www.w3.org/2001/XMLSchema",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "tl": aguide,
        "cx": aguide,
        "dc": "http://purl.org/dc/elements/1.1/",
        "mbp": aguide + "m",
        "mmc": aguide,
        "idx": aguide + "i",
    }
    attribrep = {"xmlns:" + k: v for k, v in nsmap.items()}
    htmlel = etree.Element("html", nsmap=nsmap)
    #
    htag = mkHeadTag()
    mtag = mkMetaTag()
    htag.append(mtag)
    #
    htmlel.append(htag)
    #
    btag = etree.SubElement(htmlel, "body")
    frame = etree.SubElement(btag, "{" + nsmap["mbp"] + "}" + "frameset")
    return htmlel, htag, btag, frame, nsmap, attribrep


def mkKdict(entry_parameters: List[dict]) -> str:
    "make kindle dict from kdict entries"
    html, htag, btag, frame, nsmap, attribrep = mkKdictTemplate()
    for entry_parameter in entry_parameters:
        entry = mkEntry(entry_parameter, nspace=nsmap["idx"], parent_el=frame)
        hrule = etree.Element("hr")
        frame.append(hrule)
        #
    # fix name space values
    k1, k2 = "mbp", "idx"
    nsmap[k1] = nsmap[k1][:-1]
    nsmap[k2] = nsmap[k2][:-1]
    htmlstr = etree.tostring(
        html, xml_declaration=True, pretty_print=True, encoding="utf-8"
    ).decode("utf-8")
    htmlstr = htmlstr.replace("Guidelines.pdfm", "Guidelines.pdf")
    htmlstr = htmlstr.replace("Guidelines.pdfi", "Guidelines.pdf")
    return htmlstr
