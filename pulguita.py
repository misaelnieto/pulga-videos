from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Label
from textual.validation import URL
from textual.containers import  HorizontalGroup, HorizontalScroll, Horizontal, VerticalScroll, Vertical

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Placeholder
from textual.widgets import Static
from textual.color import Gradient
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Middle
from textual.timer import Timer
from textual.widgets import Footer, ProgressBar
from pytube import YouTube



class Pulguita(App[str]):
    """Una aplicación que descarga videos y audios de Youtube"""

    CSS_PATH = "pulguita.tcss"


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Label("Pega la dirección del video de Youtube")
        with Horizontal():
            yield Input(id="url", placeholder="https://www.youtube.com/watch?v=...", validators=[URL()])
            yield Button("Descargar", id="download", variant="primary", disabled=True)
        with Center():
            yield ProgressBar(id="progress")
            yield Label("Descargando archivo...", id="file_name")

        yield Button("Salir", variant="error", id="exit")

    @property
    def progress_bar(self) -> ProgressBar:
        return self.get_widget_by_id("progress", ProgressBar)

    @property
    def file_name(self) -> Label:
        return self.get_widget_by_id("file_name", Label)

    def on_mount(self) -> None:
        self.progress_bar.display = False
        self.file_name.display = False
        

    @on(Button.Pressed, "#exit")
    def exit_pressed(self, event: Button.Pressed) -> None:
        """Exit the application"""
        self.exit()

    @on(Input.Changed)
    def enable_download_button(self, event: Input.Changed) -> None:
        download_button = self.get_widget_by_id("download", Button)
        download_button.disabled = False if event.validation_result.is_valid else True

    @on(Button.Pressed, "#download")
    def download_pressed(self, event: Button.Pressed) -> None:
        """Start downloading the video"""
        event.button.disabled = True
        url_input = self.get_widget_by_id("url", Input)
        url_input.disabled = True
        url = url_input.value
        self.progress_bar.display = True
        self.file_name.display = True
        self.start_youtube_dl(url)


    def start_youtube_dl(self, url: str):
        yt = YouTube(url, on_progress_callback=self.download_progress_cb, on_complete_callback=self.completed_cb,)
        yt.


if __name__ == "__main__":
    Pulguita().run()
