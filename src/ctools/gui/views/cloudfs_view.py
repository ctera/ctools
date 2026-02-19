"""CloudFS view - Create folder groups, cloud drive folders, and zones from CSV."""

from .base_view import BaseToolView
from ..widgets import FileField, CheckboxField, FormSection
from ...tools.cloudfs import create_folders


class CloudFSView(BaseToolView):
    """View for creating CloudFS folder groups, folders, and zones from CSV."""

    title = "CloudFS"
    description = "Create cloud folder groups, cloud drive folders, and zones from a CSV file"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("CloudFS Settings")

        self.csv_field = FileField(
            "CSV File",
            "Select CSV file with folder definitions",
            mode="open",
            file_filter="CSV Files (*.csv);;All Files (*.*)"
        )
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.csv_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.csv_field.text():
            self.output_card.appendText("Error: CSV file path is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the CloudFS tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            create_folders(
                session,
                filepath=self.csv_field.text()
            )
        finally:
            try:
                session.logout()
            except:
                pass
