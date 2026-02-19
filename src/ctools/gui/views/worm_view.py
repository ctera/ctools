"""WORM Settings view."""

from .base_view import BaseToolView
from ..widgets import FormField, PasswordField, CheckboxField, FormSection, ComboBoxField
from ...tools.worm_settings import worm_settings


class WormSettingsView(BaseToolView):
    """View for configuring WORM settings."""

    title = "WORM Settings"
    description = "Configure WORM (Write Once Read Many) compliance settings"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("WORM Configuration")

        self.folder_id_field = FormField("Folder ID", "Cloud folder ID to configure")
        self.grace_period_field = FormField("Grace Period Value", "e.g., 30")
        self.target_date_field = FormField("Target Date", "e.g., '26 Aug 2026'")
        self.operation_field = ComboBoxField("Operation", [
            "Set Grace Period",
            "Set Retention Period",
            "Lock Folder",
            "Unlock Folder"
        ])
        self.period_type_field = ComboBoxField("Period Type", [
            "Days",
            "Months",
            "Years"
        ])
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addRow(self.folder_id_field, self.grace_period_field)
        section.addField(self.target_date_field)
        section.addRow(self.operation_field, self.period_type_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.folder_id_field.text():
            self.output_card.appendText("Error: Folder ID is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the WORM settings tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            worm_settings(
                session,
                folder_id=self.folder_id_field.text(),
                operation=self.operation_field.currentText(),
                grace_period=self.grace_period_field.text() or None,
                period_type=self.period_type_field.currentText(),
                target_date=self.target_date_field.text() or None
            )
        finally:
            try:
                session.logout()
            except:
                pass
