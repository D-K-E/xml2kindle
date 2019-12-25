# make an entry for kindle dict format
# Author: Kaan Eraslan
# License: see, LICENSE
# packages
import os
from lxml import etree
import argparse
from uuid import uuid4
from datetime import date
from xml2kindle.extractor.lsj.lsjperseus import LSJPerseusDictExtractor
from xml2kindle.maker.opfmaker import DictOPF
from xml2kindle.maker.kdict.dictmaker import mkKdict
from xml2kindle.maker.kdict.entrymaker import mkEntry
import pdb


def check_proj_name(pname: str):
    "check if project name is alphanumeric"
    if not pname.isalnum():
        raise ValueError(
            "Only alphanumeric strings" + "are allowed for project names: " + pname
        )


def check_btypes(btype, btypes):
    "check if build type is available among given build types"
    if btype not in btypes.keys():
        raise ValueError(
            btype + " is unavailable, available build types are{0}".format(str(btypes))
        )


def check_extractor(extr, btype, btypes):
    "check if given extractor is available for given build type"
    if extr not in btypes[btype]:
        extmes = "Extractor " + extr + "unavailable, please do think of contributing"
        extmes += " your own extractor, if you think the project can "
        extmes += "benefit to the others."
        extmes += " Checkout the project on Github: D-K-E/xml2kindle"
        raise ValueError(extmes)


def check_tei_path_ext(tpath):
    "check if tei has xml extension"
    tname = os.path.basename(tpath)
    ext = tname.split(".")[-1]
    if ext != "xml":
        raise ValueError("Doc without xml extension: {0}".format(tpath))


def check_metadata_params(params: dict, btype):
    "check metadata parameter dict"
    if btype == "dict":
        clist = ["imtype", "impath", "index_name"]
    else:
        clist = ["imtype", "impath"]
    for pname in clist:
        if pname not in params.keys():
            raise ValueError(
                "Metadata parameters do not have a required param: " + pname
            )


class DocBuilder:
    "Document builder for xml2kindle projects"
    BUILD_TYPES = {"dict": {"lsj": LSJPerseusDictExtractor}, "book": {}}

    def __init__(
        self,
        output_dir: str,
        build_type: str,
        project_name: str,
        tei_path: str,
        extractor: str,
        metadata_params: dict,
    ):
        ""
        self.odir = output_dir
        check_proj_name(project_name)
        self.pname = project_name
        check_btypes(build_type, self.BUILD_TYPES)
        self.btype = build_type
        self.opath = os.path.join(self.odir, self.pname)
        lowex = extractor.lower()
        check_extractor(lowex, build_type, self.BUILD_TYPES)
        self.extractor = lowex
        check_tei_path_ext(tei_path)
        self.tpath = tei_path
        check_metadata_params(metadata_params, build_type)
        self.meta = metadata_params

    def save_document_content(self, name: str, content: str):
        "save document content to given path"
        spath = os.path.join(self.opath, name)
        with open(spath, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

    def mv_image(self) -> str:
        "move image to output location"
        impath = self.meta["impath"]
        imname = os.path.basename(impath)
        nimpath = os.path.join(self.opath, imname)
        os.replace(impath, nimpath)
        return nimpath

    def get_common_doc_parts(self, extractor):
        "get common document parts from extractor"
        title = extractor.get_title()
        lang = extractor.get_doc_lang()
        creator = extractor.get_creator()
        return title, creator, lang

    def build_dict(self):
        "build dictionary"
        # make output folder
        if not os.path.isdir(self.opath):
            os.mkdir(self.opath)
        # move cover image to opath
        nimpath = self.mv_image()
        imname = os.path.basename(nimpath)

        # open tei doc
        # get extractor
        DictExtractor = self.BUILD_TYPES[self.btype][self.extractor]
        extractor = DictExtractor(
            index_name=self.meta["index_name"], teipath=self.tpath
        )

        # get parts
        doc_title, doc_creator, doc_lang = self.get_common_doc_parts(extractor)
        doc_inlang = extractor.get_inlang()
        doc_outlang = extractor.get_outlang()
        entry_parameters = extractor.get_entry_parameters()
        doc_content = mkKdict(entry_parameters)

        # save document content
        doc_name = self.pname + ".xhtml"
        self.save_document_content(name=doc_name, content=doc_content)

        # make metadata
        dopf = DictOPF(
            title=doc_title,
            idstr=uuid4(),
            creator=doc_creator,
            time=date.today(),
            lang=doc_lang,
            imtype=self.meta["imtype"],
            impath=imname,
            fname=doc_name,
            inlang=doc_inlang,
            outlang=doc_outlang,
            lookup_index_name=self.meta["index_name"],
        )
        meta_content = dopf.toxml()
        meta_content_bytes = etree.tostring(
            meta_content, pretty_print=False, xml_declaration=True, encoding="utf-8"
        )
        meta_content_str = meta_content_bytes.decode("utf-8")
        meta_name = "metadata.opf"

        # save metadata
        self.save_document_content(name=meta_name, content=meta_content_str)

    def build_book(self):
        pass

    def build(self):
        "build document with given build type"
        if self.btype == "dict":
            self.build_dict()
        else:
            self.build_book()


def getArgs():
    parser = argparse.ArgumentParser(
        description="Build kindle compatible ebook or dictionary from TEI XML"
    )
    parser.add_argument("odir", help="output directory")
    parser.add_argument(
        "buildType", help="build type", choices=list(DocBuilder.BUILD_TYPES.keys())
    )
    parser.add_argument("projectName", help="alphanumeric project name")
    parser.add_argument("teiPath", help="tei document path")
    parser.add_argument(
        "teiExtractor",
        help="tei extractor. Available extractors are:",
        choices=list(DocBuilder.BUILD_TYPES["dict"].keys())
        + list(DocBuilder.BUILD_TYPES["book"].keys()),
    )
    parser.add_argument("imagePath", help="cover image path")
    parser.add_argument("imageType", help="cover image type")
    parser.add_argument(
        "indexName", help="default index name for dictionary build type"
    )
    return parser.parse_args()


def main():
    "main run of program"
    pargs = getArgs()
    mdata = {}
    if pargs.indexName:
        mdata["index_name"] = pargs.indexName
    mdata["imtype"] = pargs.imageType
    mdata["impath"] = pargs.imagePath
    odir = pargs.odir
    btype = pargs.buildType
    pname = pargs.projectName
    teipath = pargs.teiPath
    extr = pargs.teiExtractor
    builder = DocBuilder(
        output_dir=odir,
        build_type=btype,
        project_name=pname,
        tei_path=teipath,
        extractor=extr,
        metadata_params=mdata,
    )
    builder.build()
    print("Document components built to:")
    print(builder.opath)


if __name__ == "__main__":
    main()
