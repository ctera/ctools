"""SSH control views (Enable/Disable)."""

from .base_view import BaseToolView
from ..widgets import FormField, CheckboxField, FormSection
from ...tools.enable_ssh import enable_ssh
from ...tools.disable_ssh import disable_ssh


class EnableSSHView(BaseToolView):
    """View for enabling SSH on filers."""

    title = "Enable SSH"
    description = "Enable SSH access on one or more filers"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("SSH Settings")

        self.public_key_field = FormField("SSH Public Key", "Paste your SSH public key here")
        self.tenant_field = FormField("Tenant Name", "Leave blank for all tenants")
        self.device_field = FormField("Device Name", "Leave blank for all devices")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.public_key_field)
        section.addRow(self.tenant_field, self.device_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.public_key_field.text():
            self.output_card.appendText("Error: SSH public key is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the enable SSH tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            enable_ssh(
                session,
                public_key=self.public_key_field.text(),
                tenant=tenant,
                device=self.device_field.text() or None,
                all_tenants=not tenant
            )
        finally:
            try:
                session.logout()
            except:
                pass


class DisableSSHView(BaseToolView):
    """View for disabling SSH on filers."""

    title = "Disable SSH"
    description = "Disable SSH access on one or more filers"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Target Settings")

        self.tenant_field = FormField("Tenant Name", "Leave blank for all tenants")
        self.device_field = FormField("Device Name", "Leave blank for all devices")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addRow(self.tenant_field, self.device_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _execute_tool(self) -> None:
        """Execute the disable SSH tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            disable_ssh(
                session,
                tenant=tenant,
                device=self.device_field.text() or None,
                all_tenants=not tenant
            )
        finally:
            try:
                session.logout()
            except:
                pass
