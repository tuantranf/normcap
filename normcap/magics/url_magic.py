"""Magic to handle URL(s) in selection."""

# Default
import re
import os
import webbrowser

# Own
from magics.base_magic import BaseMagic
from data_model import NormcapData


class UrlMagic(BaseMagic):
    def score(self, request: NormcapData) -> float:
        """Calculate score based on chars in URLs vs. overall chars.

        Arguments:
            BaseMagic {class} -- Base class for magics
            request {NormcapData} -- NormCap's session data

        Returns:
            float -- score between 0-100 (100 = more likely)
        """
        # Get concatenated lines
        text = request.text

        # Search urls in line
        # (Creds to http://www.regexguru.com/2008/11/detecting-urls-in-a-block-of-text/)
        reg_url = (
            r"(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)"  # Prefix
            r"(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*"  # Handling parenthesis
            r"(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])"
        )
        self.urls = re.findall(reg_url, text, flags=re.IGNORECASE)
        self._logger.info(f"{len(self.urls)} URLs found:\n{self.urls}")

        # Calc chars & ratio
        url_chars = sum([len(e) for e in self.urls])
        overall_chars = len(text)
        ratio = url_chars / overall_chars
        self._logger.info(
            f"{url_chars} of {overall_chars} chars in emails (ratio: {ratio})"
        )

        # Map to score
        self._final_score = round(100 * ratio, 2)

        return self._final_score

    def transform(self, request: NormcapData) -> str:
        """Parse URLs and return as newline separated string.

        Arguments:
            request {NormcapData} -- NormCap's session data

        Returns:
            str -- URL(s), separated bye newline
        """
        self._logger.info("Transforming with URL magic...")

        # www. often is falsly ocr-ed as WWW. (capitals). Let's fix that:
        self.urls = [u.replace("WWW.", "www.") for u in self.urls]

        # Return as line separated list
        return os.linesep.join(self.urls)

    def trigger(self, request: NormcapData):
        """Open URL(s) in new tab(s) with default browser.

        Arguments:
            request {NormcapData} -- NormCap's session data
        """
        self._logger.info("Open URL(s) in Browser...")
        urls = request.transformed.split(os.linesep)  # TODO: Better use self.urls?
        for url in urls:
            webbrowser.open_new_tab(f"{url}")