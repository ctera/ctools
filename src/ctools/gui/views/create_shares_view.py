"""Create Shares from CSV view - Create shares with ACLs on a filer from CSV."""

from .base_view import BaseToolView
from ..widgets import FormField, FileField, CheckboxField, FormSection
from ...tools.create_shares import create_shares_from_csv


class CreateSharesView(BaseToolView):
    """View for creating shares with ACL entries from a CSV file."""

    title = "Create Shares"
    description = "Create shares with permissions on a filer from a CSV file"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Share Settings")

        self.device_field = FormField(
            "Device Name",
            "Name of the target filer device"
        )
        self.tenant_field = FormField(
            "Tenant Name",
            "Leave blank if not needed"
        )
        self.csv_field = FileField(
            "CSV File",
            "Select CSV file with share definitions",
            mode="open",
            file_filter="CSV Files (*.csv);;All Files (*.*)"
        )
        self.exclude_everyone_checkbox = CheckboxField("Exclude Everyone RW")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.device_field)
        section.addField(self.tenant_field)
        section.addField(self.csv_field)
        section.addField(self.exclude_everyone_checkbox)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.device_field.text():
            self.output_card.appendText("Error: Device name is required\n")
            return False
        if not self.csv_field.text():
            self.output_card.appendText("Error: CSV file path is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the create shares from CSV tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            create_shares_from_csv(
                session,
                device=self.device_field.text(),
                filepath=self.csv_field.text(),
                tenant=self.tenant_field.text() or None,
                exclude_everyone_rw=self.exclude_everyone_checkbox.isChecked(),
            )
        finally:
            try:
                session.logout()
            except:
                pass
