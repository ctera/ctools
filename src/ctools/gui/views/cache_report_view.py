"""Cache Report view."""

from pathlib import Path

from .base_view import BaseToolView
from ..widgets import FormField, FileField, CheckboxField, FormSection
from ...core.auth import enable_device_sso, global_admin_login
from ...tools.cache_report import run_cache_report


class CacheReportView(BaseToolView):
    """View for edge filer cache utilization reports."""

    title = "Cache Report"
    description = (
        "Uses the same connected-filer list and portal device API as Status Report "
        "(no direct edge SSO / remoteAccessUrl)."
    )

    def _create_tool_section(self) -> None:
        section = FormSection("Report Settings")

        default_out = Path.home() / "Documents" / "CTools-reports" / "cache_report.csv"
        self.filename_field = FileField(
            "Output File",
            "e.g., cache_report.csv",
            mode="save",
            file_filter="CSV Files (*.csv);;All Files (*.*)",
        )
        self.filename_field.setText(str(default_out))
        self.tenant_field = FormField("Tenant Name", "Leave blank when scanning all portals")
        self.input_csv_field = FileField(
            "Input CSV (optional)",
            "device_name,tenant — leave blank to scan filers",
            mode="open",
            file_filter="CSV Files (*.csv);;All Files (*.*)",
        )
        self.all_tenants_checkbox = CheckboxField("All portals / tenants")
        self.all_tenants_checkbox.setChecked(True)
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.filename_field)
        section.addField(self.tenant_field)
        section.addField(self.input_csv_field)
        section.addField(self.all_tenants_checkbox)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        if not super()._validate_inputs():
            return False
        if not self.filename_field.text():
            self.output_card.appendText("Error: Output filename is required\n")
            return False
        out = Path(self.filename_field.text().strip())
        if out.is_dir():
            self.output_card.appendText("Error: Output path must be a file, not a folder\n")
            return False
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            self.output_card.appendText(f"Error: Cannot write to output file: {exc}\n")
            return False
        if not self.input_csv_field.text() and not self.all_tenants_checkbox.isChecked():
            if not self.tenant_field.text():
                self.output_card.appendText(
                    "Error: Specify a tenant, enable All portals, or provide an input CSV\n"
                )
                return False
        return True

    def _execute_tool(self) -> None:
        # Match standalone edge_filer_cache_report: one GlobalAdmin session for SSO + remote_access.
        address = self.address_field.text()
        username = self.username_field.text()
        password = self.password_field.text()
        session = global_admin_login(address, username, password, ignore_cert=True)
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            enable_device_sso(session)
            tenant = self.tenant_field.text() or None
            input_csv = self.input_csv_field.text() or None
            run_cache_report(
                session,
                filename=self.filename_field.text(),
                tenant=tenant,
                all_tenants=self.all_tenants_checkbox.isChecked(),
                input_csv=input_csv,
            )
        finally:
            try:
                session.logout()
            except Exception:
                pass
