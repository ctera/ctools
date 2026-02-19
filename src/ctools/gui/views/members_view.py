"""Add/Remove Members view - Manage Administrators group membership on filers."""

from .base_view import BaseToolView
from ..widgets import FormField, CheckboxField, FormSection, ComboBoxField
from ...tools.add_remove_members import add_remove_members


class AddRemoveMembersView(BaseToolView):
    """View for adding/removing domain users/groups to Administrators group."""

    title = "Add/Remove Members"
    description = "Add or remove domain users/groups to/from Administrators group on filers"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Member Settings")

        self.operation_field = ComboBoxField("Operation", ["Add", "Remove"])
        self.user_field = FormField("Domain User", "e.g., domain\\username or username")
        self.group_field = FormField("Domain Group", "e.g., domain\\groupname or groupname")
        self.tenant_field = FormField("Tenant Name", "Leave blank for all tenants")
        self.device_field = FormField("Device Name", "Leave blank for all devices in tenant")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.operation_field)
        section.addRow(self.user_field, self.group_field)
        section.addRow(self.tenant_field, self.device_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.user_field.text() and not self.group_field.text():
            self.output_card.appendText("Error: Either domain user or domain group is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the add/remove members tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            device = self.device_field.text() or None

            add_remove_members(
                session,
                operation=self.operation_field.currentText(),
                user=self.user_field.text() or None,
                group=self.group_field.text() or None,
                tenant=tenant,
                device=device,
                all_tenants=not tenant and not device
            )
        finally:
            try:
                session.logout()
            except:
                pass
