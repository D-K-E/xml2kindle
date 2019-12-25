# make an entry for kindle dict format
# Author: Kaan Eraslan
# License: see, LICENSE
# packages
import os
from lxml import etree

# end packages


def mkEntryContainer(
    lookup_index_name: str, idstr: str, nspace: str, parent_el: etree.Element
) -> etree.Element:
    "make an entry container idx:entry"
    econt = etree.SubElement(parent_el, "{" + nspace + "}entry")
    econt.set("name", lookup_index_name)
    econt.set("scriptable", "yes")
    econt.set("spell", "yes")
    econt.set("id", idstr)
    return econt


def mkEntryAnchor(
    anchor_id: str, nspace: str, parent_el: etree.Element
) -> etree.Element:
    "make entry anchor idx:short, a etc"
    short = etree.SubElement(parent_el, "{" + nspace + "}short")
    anc = etree.Element("a")
    anc.set("id", anchor_id)
    short.append(anc)
    return short


def mkEntryLabel(
    attrval: str, display_val: str, nspace: str, parent_el: etree.Element
) -> etree.Element:
    "index label of entry idx:orth tag"
    elbl = etree.SubElement(parent_el, "{" + nspace + "}orth")
    elbl.set("value", attrval)
    elbl.text = display_val
    return elbl


def mkInflectionForm(
    name: str, val: str, isExcat: str, nspace: str, parent_el: etree.Element
) -> etree.Element:
    "make inflection form"
    infel = etree.SubElement(parent_el, "{" + nspace + "}iform")
    infel.set("name", name)
    infel.set("value", val)
    infel.set("excat", isExcat)
    return infel


def mkInflectionEl(nspace: str, parent_el: etree.Element) -> etree.Element:
    return etree.SubElement(parent_el, "{" + nspace + "}infl")


def addInflection2Infel(
    infel: etree.Element, name: str, val: str, nspace: str, isExcat="no"
) -> etree.Element:
    "add inflection to given inflection element"
    iform = mkInflectionForm(name, val, isExcat, nspace, parent_el=infel)
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


def getInflections(inflections: list, nspace: str, parent_el: etree.Element):
    "make Inflection forms from inflection parameters"
    infel = mkInflectionEl(nspace, parent_el=parent_el)
    for inflection_params in inflections:
        if inflection_params.get("isExcat") is not None:
            isExcat = inflection_params["isExcat"]
        else:
            isExcat = "no"
        infname = inflection_params["name"]
        infval = inflection_params["value"]
        addInflection2Infel(infel, infname, infval, nspace, isExcat)
    return infel


def mkEntry(entry_params: dict, nspace: str, parent_el: etree.Element) -> etree.Element:
    """mk entry using entry parameters
    for entry_params dictionary see
    entry.json in assets/template/entry.json
    
    """
    index_name = entry_params["index"]
    seq_id = entry_params["id"]
    #
    contel = mkEntryContainer(index_name, seq_id, nspace=nspace, parent_el=parent_el)
    shortel = mkEntryAnchor(seq_id, nspace=nspace, parent_el=contel)
    #
    entryval = entry_params["value"]
    displayval = entry_params["display_value"]
    orthel = mkEntryLabel(entryval, displayval, nspace=nspace, parent_el=shortel)
    #
    inflections = entry_params.get("inflections")
    if inflections is not None:
        infel = getInflections(inflections, nspace=nspace, parent_el=orthel)
    #
    defvals = entry_params["definitions"]
    for i, defval in enumerate(defvals):
        defel = mkDefinition(defval, str(i))
        shortel.append(defel)
    #
    othertags = entry_params.get("other")
    if othertags is not None:
        for other in othertags:
            shortel.append(other)
    return contel
