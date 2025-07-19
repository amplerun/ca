// This file is the single source of truth for all permissions in the system.
// It is shared between the frontend and backend.

export const Permissions = {
  // Admin & User Management
  MANAGE_USERS: 'manage_users', // Create, update, delete users
  MANAGE_ROLES: 'manage_roles', // Create, update, delete roles and their permissions
  VIEW_ADMIN_PANEL: 'view_admin_panel',

  // System Admin
  MANAGE_PROMPTS: 'manage_prompts', // Edit AI prompts for the company

  // Audit
  VIEW_AUDIT_LOGS: 'view_audit_logs',

  // Accounting
  CREATE_JOURNAL_ENTRY: 'create_journal_entry',
  VIEW_JOURNAL: 'view_journal',
  VIEW_LEDGER: 'view_ledger',
  VIEW_TRIAL_BALANCE: 'view_trial_balance',
  GENERATE_PL_REPORT: 'generate_pl_report',
  GENERATE_BS_REPORT: 'generate_bs_report',

  // GST
  FILE_GST_RETURN: 'file_gst_return',
  VIEW_GST_REPORTS: 'view_gst_reports',

  // Direct Tax
  COMPUTE_TAX: 'compute_tax',
  FILE_ITR: 'file_itr',

  // Payroll
  RUN_PAYROLL: 'run_payroll',
  VIEW_PAYROLL_REPORTS: 'view_payroll_reports',

  // ROC
  FILE_ROC: 'file_roc',
  VIEW_ROC_FILINGS: 'view_roc_filings',
} as const;

export type Permission = (typeof Permissions)[keyof typeof Permissions];

export const ALL_PERMISSIONS = Object.values(Permissions) as Permission[];

export const DefaultRoles = {
  Admin: {
    name: 'Admin',
    description: 'Has all permissions and can manage the system.',
    permissions: ALL_PERMISSIONS,
  },
  ElevatedUser: {
    name: 'ElevatedUser',
    description: 'Can perform most financial tasks but cannot manage users or system settings.',
    permissions: [
      Permissions.CREATE_JOURNAL_ENTRY,
      Permissions.VIEW_JOURNAL,
      Permissions.VIEW_LEDGER,
      Permissions.VIEW_TRIAL_BALANCE,
      Permissions.GENERATE_PL_REPORT,
      Permissions.GENERATE_BS_REPORT,
      Permissions.FILE_GST_RETURN,
      Permissions.VIEW_GST_REPORTS,
      Permissions.COMPUTE_TAX,
      Permissions.FILE_ITR,
      Permissions.RUN_PAYROLL,
      Permissions.VIEW_PAYROLL_REPORTS,
      Permissions.FILE_ROC,
      Permissions.VIEW_ROC_FILINGS,
    ],
  },
  NormalUser: {
    name: 'NormalUser',
    description: 'Can view reports and perform basic data entry.',
    permissions: [
      Permissions.CREATE_JOURNAL_ENTRY,
      Permissions.VIEW_JOURNAL,
      Permissions.VIEW_LEDGER,
      Permissions.VIEW_TRIAL_BALANCE,
      Permissions.GENERATE_PL_REPORT,
      Permissions.GENERATE_BS_REPORT,
      Permissions.VIEW_GST_REPORTS,
      Permissions.VIEW_PAYROLL_REPORTS,
      Permissions.VIEW_ROC_FILINGS,
    ],
  },
  ReadOnlyUser: {
    name: 'ReadOnlyUser',
    description: 'Can only view data and reports.',
    permissions: [
        Permissions.VIEW_JOURNAL,
        Permissions.VIEW_LEDGER,
        Permissions.VIEW_TRIAL_BALANCE,
        Permissions.GENERATE_PL_REPORT,
        Permissions.GENERATE_BS_REPORT,
        Permissions.VIEW_GST_REPORTS,
        Permissions.VIEW_PAYROLL_REPORTS,
        Permissions.VIEW_ROC_FILINGS,
    ],
  }
};