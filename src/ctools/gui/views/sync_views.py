"""Sync control views (Suspend/Unsuspend)."""

from .base_view import BaseToolView
from ..widgets import FormField, CheckboxField, FormSection
from ...tools.suspend_sync import suspend_sync
from ...tools.unsuspend_sync import unsuspend_sync


class SuspendSyncView(BaseToolView):
    """View for suspending cloud sync on filers."""

    title = "Suspend Sync"
    description = "Pause cloud synchronization on one or more filers"

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
        """Execute the suspend sync tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            suspend_sync(
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


class UnsuspendSyncView(BaseToolView):
    """View for resuming cloud sync on filers."""

    title = "Resume Sync"
    description = "Resume cloud synchronization on one or more filers"

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
        """Execute the unsuspend sync tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            tenant = self.tenant_field.text() or None
            unsuspend_sync(
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
