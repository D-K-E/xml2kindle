# kindle dict maker which conforms to kindle publishing guidelines
# Author: Kaan Eraslan
# License: see, LICENSE

from lxml import etree
from typing import List


def mkKdictTemplate() -> etree.Element:
    "make kindle dictionary template to be filled by entries"
    return etree.XML(
        """
<html xmlns:math="http://exslt.org/math" xmlns:svg="http://www.w3.org/2000/svg" xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:saxon="http://saxon.sf.net/" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>

<body>
    <mbp:frameset></mbp:frameset>
</body>

</html>
    """
    )


def mkKdict(entries: List[etree.Element]):
    "make kindle dict from kdict entries"
    template = mkKdictTemplate()
    for btag in template.iter("body"):
        mbtag = btag[0]
        for entry in entries:
            mbtag.append(entry)
            hrule = etree.Element("hr")
            mbtag.append(hrule)
        #
    return template
