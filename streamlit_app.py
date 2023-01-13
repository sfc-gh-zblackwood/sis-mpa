from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import streamlit as st
from streamlit.source_util import _on_pages_changed, get_pages, page_icon_and_name
from streamlit.util import calc_md5


@dataclass
class Page:
    """
    Utility class for working with pages
    Parameters
    ----------
    path: str
        The path to the page
    name: str (optional)
        The name of the page. If not provided, the name will be inferred from
        the path
    icon: str (optional)
        The icon of the page. If not provided, the icon will be inferred from
        the path
    """

    path: str
    name: str | None = None
    icon: str | None = None

    @property
    def page_path(self) -> Path:
        return Path(str(self.path))

    @property
    def page_name(self) -> str:
        standard_name = page_icon_and_name(self.page_path)[1]
        standard_name = standard_name.replace("_", " ").title()
        if self.name is None:
            return standard_name
        return self.name

    @property
    def page_icon(self) -> str:
        standard_icon = page_icon_and_name(self.page_path)[0]
        icon = self.icon or standard_icon or ""
        return icon

    @property
    def page_hash(self) -> str:
        return calc_md5(str(self.page_path))

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "page_script_hash": self.page_hash,
            "page_name": self.page_name,
            "icon": self.page_icon,
            "script_path": str(self.page_path),
        }

    @classmethod
    def from_dict(cls, page_dict: dict[str, str | bool]) -> Page:
        return cls(
            path=str(page_dict["script_path"]),
            name=str(page_dict["page_name"]),
            icon=str(page_dict["icon"]),
        )


def show_pages(pages: list[Page]):
    """
    Given a list of Page objects, overwrite whatever pages are currently being
    shown in the sidebar, and overwrite them with this new set of pages.
    NOTE: This changes the list of pages globally, not just for the current user, so
    it is not appropriate for dymaically changing the list of pages.
    """
    current_pages: dict[str, dict[str, str | bool]] = get_pages("")  # type: ignore
    if set(current_pages.keys()) == set(p.page_hash for p in pages):
        return

    try:
        [p.path for p in pages if p.path][0]
    except IndexError:
        raise ValueError("Must pass at least one page to show_pages")

    current_pages.clear()
    for page in pages:
        current_pages[page.page_hash] = page.to_dict()

    _on_pages_changed.send()


st.title("MultiPage App Example")
st.subheader("Most of the code copied straight from https://github.com/blackary/st_pages")

show_pages(
    [
        Page("streamlit_app.py", "Home", "🏠"),
        Page("secondary_page.py", "Secondary Page", "📄"),
    ]
)
