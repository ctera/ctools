"""Status Report view."""

from .base_view import BaseToolView
from ..widgets import FormField, FileField, CheckboxField, FormSection
from ...tools.status import run_status


class StatusView(BaseToolView):
    """View for generating filer status reports."""

    title = "Status Report"
    description = "Generate comprehensive status reports for all connected filers"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Report Settings")

        self.filename_field = FileField(
            "Output File",
            "e.g., status_report.csv",
            mode="save",
            file_filter="CSV Files (*.csv);;All Files (*.*)"
        )
        self.tenant_field = FormField("Tenant Name", "Leave blank for all tenants")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.filename_field)
        section.addField(self.tenant_field)
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
        """Execute the status report tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            run_status(
                session,
                filename=self.filename_field.text(),
                tenant=tenant,
                all_tenants=not tenant
            )
        finally:
            try:
                session.logout()
            except:
                pass
