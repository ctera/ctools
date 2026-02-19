"""Zones Report view."""

from .base_view import BaseToolView
from ..widgets import FileField, CheckboxField, FormSection
from ...tools.report_zones import report_zones


class ReportZonesView(BaseToolView):
    """View for generating zones reports."""

    title = "Zones Report"
    description = "Generate a report of all zones in the portal"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Report Settings")

        self.filename_field = FileField(
            "Output File",
            "e.g., zones_report.csv",
            mode="save",
            file_filter="CSV Files (*.csv);;All Files (*.*)"
        )
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.filename_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.filename_field.text():
            self.output_card.appendText("Error: Output filename is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the zones report tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            report_zones(
                session,
                filename=self.filename_field.text()
            )
        finally:
            try:
                session.logout()
            except:
                pass
