"""ID Mapping view."""

from .base_view import BaseToolView
from ..widgets import FormField, CheckboxField, FormSection
from ...tools.add_mapping import add_mapping


class AddMappingView(BaseToolView):
    """View for adding domain to ID mapping."""

    title = "ID Mapping"
    description = "Add domain to advanced ID mapping on filers"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Mapping Settings")

        self.domain_field = FormField("Domain Name", "e.g., company.com")
        self.tenant_field = FormField("Tenant Name", "Leave blank for all tenants")
        self.device_field = FormField("Device Name", "Leave blank for all devices")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.domain_field)
        section.addRow(self.tenant_field, self.device_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.domain_field.text():
            self.output_card.appendText("Error: Domain name is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the add mapping tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            add_mapping(
                session,
                domain=self.domain_field.text(),
                tenant=tenant,
                device=self.device_field.text() or None,
                all_tenants=not tenant
            )
        finally:
            try:
                session.logout()
            except:
                pass
