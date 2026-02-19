"""Run Command view."""

from typing import Optional
from PySide6.QtWidgets import QWidget

from .base_view import BaseToolView
from ..widgets import FormField, CheckboxField, FormSection
from ...tools.run_cmd import run_cmd


class RunCmdView(BaseToolView):
    """View for running CLI commands on filers."""

    title = "Run Command"
    description = "Execute CLI commands on one or more connected filers"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Command Settings")

        self.command_field = FormField("Command", "e.g., show /config/device")
        self.tenant_field = FormField("Tenant Name", "Leave blank for all tenants")
        self.device_field = FormField("Device Name", "Leave blank for all devices")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.command_field)
        section.addRow(self.tenant_field, self.device_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.command_field.text():
            self.output_card.appendText("Error: Command is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the run command tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            device = self.device_field.text() or None

            run_cmd(
                session,
                command=self.command_field.text(),
                tenant=tenant,
                device=device,
                all_tenants=not tenant
            )
        finally:
            try:
                session.logout()
            except:
                pass
