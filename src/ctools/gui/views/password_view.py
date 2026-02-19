"""Reset Password view."""

from .base_view import BaseToolView
from ..widgets import FormField, PasswordField, CheckboxField, FormSection
from ...tools.reset_password import reset_password


class ResetPasswordView(BaseToolView):
    """View for resetting passwords on filers."""

    title = "Reset Password"
    description = "Reset local user passwords on one or more filers"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Password Settings")

        self.username_field = FormField("Username", "Local username (default: admin)")
        self.new_password_field = PasswordField("New Password", "Enter new password")
        self.tenant_field = FormField("Tenant Name", "Leave blank for all tenants")
        self.device_field = FormField("Device Name", "Leave blank for all devices")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.username_field)
        section.addField(self.new_password_field)
        section.addRow(self.tenant_field, self.device_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.new_password_field.text():
            self.output_card.appendText("Error: New password is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the reset password tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            reset_password(
                session,
                new_password=self.new_password_field.text(),
                username=self.username_field.text() or "admin",
                tenant=tenant,
                device=self.device_field.text() or None,
                all_tenants=not tenant
            )
        finally:
            try:
                session.logout()
            except:
                pass
