# This file is the single source of truth for all permissions in the system.
# It is shared between the Python services.

from typing import Final, List, Literal

class Permissions:
    # Admin & User Management
    MANAGE_USERS: Final = 'manage_users'
    MANAGE_ROLES: Final = 'manage_roles'
    VIEW_ADMIN_PANEL: Final = 'view_admin_panel'

    # System Admin
    MANAGE_PROMPTS: Final = 'manage_prompts'

    # Audit
    VIEW_AUDIT_LOGS: Final = 'view_audit_logs'

    # Accounting
    CREATE_JOURNAL_ENTRY: Final = 'create_journal_entry'
    VIEW_JOURNAL: Final = 'view_journal'
    VIEW_LEDGER: Final = 'view_ledger'
    VIEW_TRIAL_BALANCE: Final = 'view_trial_balance'
    GENERATE_PL_REPORT: Final = 'generate_pl_report'
    GENERATE_BS_REPORT: Final = 'generate_bs_report'

    # GST
    FILE_GST_RETURN: Final = 'file_gst_return'
    VIEW_GST_REPORTS: Final = 'view_gst_reports'

    # Direct Tax
    COMPUTE_TAX: Final = 'compute_tax'
    FILE_ITR: Final = 'file_itr'

    # Payroll
    RUN_PAYROLL: Final = 'run_payroll'
    VIEW_PAYROLL_REPORTS: Final = 'view_payroll_reports'

    # ROC
    FILE_ROC: Final = 'file_roc'
    VIEW_ROC_FILINGS: Final = 'view_roc_filings'

    @classmethod
    def get_all(cls) -> List[str]:
        return [
            value for name, value in vars(cls).items()
            if not name.startswith("_") and isinstance(value, str)
        ]

Permission = Literal[
    'manage_users', 'manage_roles', 'view_admin_panel', 'manage_prompts',
    'view_audit_logs', 'create_journal_entry', 'view_journal', 'view_ledger',
    'view_trial_balance', 'generate_pl_report', 'generate_bs_report',
    'file_gst_return', 'view_gst_reports', 'compute_tax', 'file_itr',
    'run_payroll', 'view_payroll_reports', 'file_roc', 'view_roc_filings'
]

ALL_PERMISSIONS: List[Permission] = Permissions.get_all()