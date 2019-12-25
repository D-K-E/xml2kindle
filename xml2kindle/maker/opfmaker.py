# make opf file that conforms to kindle dict format
# Author: Kaan Eraslan
# License: see, LICENSE
# packages
import os
from lxml import etree

# end packages


class OPF:
    "opf object for holding metadata related to document"

    def __init__(
        self,
        title: str,
        idstr: str,
        creator: str,
        time: str,
        lang: str,
        imtype: str,
        impath,
        fname: str,
    ):
        self.idstr = idstr
        self.title = title
        self.creator = creator
        self.time = time
        self.lang = lang
        self.imtype = imtype
        self.impath = impath
        self.fname = fname

    def get_package(self):
        return etree.XML(
            """
        <package version="2.0"
            xmlns="http://www.idpf.org/2007/opf" 
            unique-identifier="pub-id">
            <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
                <dc:identifier id="pub-id">urn:uuid:{0}</dc:identifier>
                <dc:title id="t1">{1}</dc:title>
                <meta refines="#t1" property="title-type">main</meta>
                <dc:language>{2}</dc:language>
                <dc:creator id="c1">{3}</dc:creator>
                <meta refines="#c1" property="role" scheme="marc:relators" id="role">aut</meta>
                <meta property="dcterms:modified">{4}</meta>
            </metadata>
            <manifest>
                <item id="cimage" media-type="image/{5}" href="{6}" properties="cover-image"/>
                <item id="docfile" media-type="application/xhtml+xml" href="{7}"/>
            </manifest>
            <spine>
                <itemref idref="docfile"/>
            </spine>
        </package>
            """.format(
                self.idstr,
                self.title,
                self.lang,
                self.creator,
                self.time,
                self.imtype,
                self.impath,
                self.fname,
            )
        )


class DictOPF(OPF):
    def __init__(
        self,
        title: str,  # from tei
        idstr: str,  # from program
        creator: str,  # from tei
        time: str,  # from program
        lang: str,  # from tei
        imtype: str,  # from user
        impath: str,  # from user
        fname: str,  # from program
        inlang: str,  # from tei
        outlang: str,  # from tei
        lookup_index_name: str,  # from user
    ):
        super().__init__(title, idstr, creator, time, lang, imtype, impath, fname)
        self.idstr = idstr
        self.title = title
        self.creator = creator
        self.time = time
        self.lang = lang
        self.imtype = imtype
        self.impath = impath
        self.fname = fname
        self.ilang = inlang
        self.olang = outlang
        self.iname = lookup_index_name

    def makeMetaDataLang(self):
        "make metadata elements of dictionary"
        dinel = etree.Element("DictionaryInLanguage")
        dinel.text = self.ilang
        doutel = etree.Element("DictionaryOutLanguage")
        doutel.text = self.olang
        dlookel = etree.Element("DefaultLookupIndex")
        dlookel.text = self.iname
        return [dinel, doutel, dlookel]

    def makeXmetadaPackage(self):
        "add metadata about language to opf package tag"
        dictels = self.makeMetaDataLang()
        packel = self.get_package()
        xmeta = etree.Element("x-metadata")
        for dicel in dictels:
            xmeta.append(dicel)
        packel.append(xmeta)
        return packel

    def toxml(self):
        return self.makeXmetadaPackage()

    def save(self, path: str):
        "save opf to path"
        mystr = etree.tostring(
            self.toxml(), pretty_print=True, encoding="utf-8", xml_declaration=True
        )
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(mystr)
