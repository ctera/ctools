"""Telnet control view."""

from .base_view import BaseToolView
from ..widgets import FormField, CheckboxField, FormSection
from ...tools.enable_telnet import enable_telnet


class EnableTelnetView(BaseToolView):
    """View for enabling telnet on filers."""

    title = "Enable Telnet"
    description = "Enable telnet access on one or more filers"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Telnet Settings")

        self.code_field = FormField("Required Code", "Authorization code for telnet access")
        self.tenant_field = FormField("Tenant Name", "Leave blank for all tenants")
        self.device_field = FormField("Device Name", "Leave blank for all devices")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.code_field)
        section.addRow(self.tenant_field, self.device_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.code_field.text():
            self.output_card.appendText("Error: Required code is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the enable telnet tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            enable_telnet(
                session,
                code=self.code_field.text(),
                tenant=tenant,
                device=self.device_field.text() or None,
                all_tenants=not tenant
            )
        finally:
            try:
                session.logout()
            except:
                pass
