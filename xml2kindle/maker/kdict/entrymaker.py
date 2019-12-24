# make an entry for kindle dict format
# Author: Kaan Eraslan
# License: see, LICENSE
# packages
import os
from lxml import etree

# end packages


def mkEntryContainer(lookup_index_name: str, idstr: str) -> etree.Element:
    "make an entry container idx:entry"
    econt = etree.XML("<idx:entry/>")
    econt.set("name", lookup_index_name)
    econt.set("scriptable", "yes")
    econt.set("spell", "yes")
    econt.set("id", idstr)
    return econt


def mkEntryAnchor(anchor_id: str) -> etree.Element:
    "make entry anchor idx:short, a etc"
    short = etree.XML("<idx:short/>")
    anc = etree.Element("a")
    anc.set("id", anchor_id)
    short.append(anc)
    return short


def mkEntryLabel(attrval: str, display_val: str) -> etree.Element:
    "index label of entry idx:orth tag"
    elbl = etree.XML("<idx:orth/>")
    elbl.set("value", attrval)
    elbl.text = display_val
    return elbl


def mkInflectionForm(name: str, val: str, isExcat: str) -> etree.Element:
    "make inflection form"
    infel = etree.Element("<idx:iform/>")
    infel.set("name", name)
    infel.set("value", val)
    infel.set("excat", isExcat)
    return infel


def mkInflectionEl() -> etree.Element:
    return etree.Element("<idx:infl/>")


def addInflection2Infel(
    infel: etree.Element, name: str, val: str, isExcat="no"
) -> etree.Element:
    "add inflection to given inflection element"
    iform = mkInflectionForm(name, val, isExcat)
    infel.append(iform)
    return infel


def mkDefinition(val: str, defno=None) -> etree.Element:
    "make definition"
    defel = etree.Element("p")
    defel.set("class", "sense")
    if defno is not None:
        defel.set("data-nb", "defno-" + defno)
    else:
        defel.set("data-nb", "defno-0")
    defel.text = val
    return defel


def getInflections(inflections: list):
    "make Inflection forms from inflection parameters"
    infel = mkInflectionEl()
    for inflection_params in inflections:
        if inflection_params.get("isExcat") is not None:
            isExcat = inflection_params["isExcat"]
        else:
            isExcat = "no"
        infname = inflection_params["name"]
        infval = inflection_params["value"]
        addInflection2Infel(infel, infname, infval, isExcat)
    return infel


def mkEntry(entry_params: dict) -> etree.Element:
    """mk entry using entry parameters
    for entry_params dictionary see
    entry.json in assets/template/entry.json
    
    """
    index_name = entry_params["index"]
    seq_id = entry_params["id"]
    #
    contel = mkEntryContainer(index_name, seq_id)
    shortel = mkEntryAnchor(seq_id)
    #
    entryval = entry_params["value"]
    displayval = entry_params["display_value"]
    orthel = mkEntryLabel(entryval, displayval)
    #
    inflections = entry_params.get("inflections")
    if inflections is not None:
        infel = getInflections(inflections)
        orthel.append(infel)
    #
    shortel.append(orthel)
    defvals = entry_params["definitions"]
    for i, defval in enumerate(defvals):
        defel = mkDefinition(defval, str(i))
        shortel.append(defel)
    #
    othertags = entry_params.get("other")
    if othertags is not None:
        for other in othertags:
            shortel.append(other)
    contel.append(shortel)
    return contel
