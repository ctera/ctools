"""Delete Shares view - Delete shares based on substring match."""

from .base_view import BaseToolView
from ..widgets import FormField, FileField, CheckboxField, FormSection
from ...tools.delete_shares import delete_shares


class DeleteSharesView(BaseToolView):
    """View for deleting shares based on substring match."""

    title = "Delete Shares"
    description = "Delete shares from filers based on a substring match in share names"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Delete Settings")

        self.substring_field = FormField(
            "Substring to Match",
            "Enter the substring to match in share names"
        )
        self.output_file_field = FileField(
            "Output Log File",
            "e.g., deleted_shares.csv",
            mode="save",
            file_filter="CSV Files (*.csv);;All Files (*.*)"
        )
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.substring_field)
        section.addField(self.output_file_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.substring_field.text():
            self.output_card.appendText("Error: Substring to match is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the delete shares tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            output_file = self.output_file_field.text() or "deleted_shares.csv"
            results = delete_shares(
                session,
                substring=self.substring_field.text(),
                output_file=output_file
            )

            # Report results
            if results:
                deleted = sum(1 for r in results if r[2] == 'Deleted')
                failed = sum(1 for r in results if r[2] == 'NotDeleted')
                self.output_card.appendText(
                    f"\nProcessed {len(results)} shares: {deleted} deleted, {failed} failed\n"
                )
        finally:
            try:
                session.logout()
            except:
                pass
