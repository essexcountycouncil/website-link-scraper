from urllib.parse import urlparse
import scrapy

FOLLOW_DOMAIN = "essexlocaloffer.org.uk"


class AssetSpider(scrapy.Spider):
    name = "assets"
    start_urls = ["http://www.essexlocaloffer.org.uk/"]

    def parse(self, response):
        yield {"url": response.url}

        # Follow a href to find new pages
        for link in response.xpath("//a/@href").extract():
            relative = False
            # We want to stay within the same site, consider a link to be relative if
            # it has a path but no host or scheme.
            # This excludes URIs like //www.example.com and mailto:example@example.com
            parsed = urlparse(link)
            relative = parsed.path and not parsed.netloc and not parsed.scheme
            # Follow the link if it's relative or if it's absolute within our domain
            if parsed.hostname:
                if parsed.hostname in (FOLLOW_DOMAIN, f"www.{FOLLOW_DOMAIN}"):
                    relative = True
            if relative:
                # Skip non-HTML
                if link.split(".")[-1] in (
                    "mp4",
                    "pdf",
                    "docx",
                    "doc",
                    "xls",
                    "xlsx",
                    "ppt",
                    "pptx",
                ):
                    # These files will be repeated in output.csv - need to remove these later
                    yield {"url": link}
                    continue

                yield response.follow(link, callback=self.parse)
