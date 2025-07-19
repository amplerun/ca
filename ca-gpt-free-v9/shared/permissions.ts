export const Permissions = {
  MANAGE_USERS: 'manage_users',
  MANAGE_ROLES: 'manage_roles',
  VIEW_ADMIN_PANEL: 'view_admin_panel',
  MANAGE_PROMPTS: 'manage_prompts',
  VIEW_AUDIT_LOGS: 'view_audit_logs',
  CREATE_JOURNAL_ENTRY: 'create_journal_entry',
  VIEW_JOURNAL: 'view_journal',
  VIEW_LEDGER: 'view_ledger',
  VIEW_TRIAL_BALANCE: 'view_trial_balance',
  GENERATE_PL_REPORT: 'generate_pl_report',
  GENERATE_BS_REPORT: 'generate_bs_report',
  FILE_GST_RETURN: 'file_gst_return',
  VIEW_GST_REPORTS: 'view_gst_reports',
  COMPUTE_TAX: 'compute_tax',
  FILE_ITR: 'file_itr',
  RUN_PAYROLL: 'run_payroll',
  VIEW_PAYROLL_REPORTS: 'view_payroll_reports',
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
      Permissions.GENERATE_PL_REPORT,
      Permissions.GENERATE_BS_REPORT,
      Permissions.FILE_GST_RETURN,
      Permissions.COMPUTE_TAX,
      Permissions.RUN_PAYROLL,
      Permissions.FILE_ROC,
    ],
  },
  NormalUser: {
    name: 'NormalUser',
    description: 'Can view reports and perform basic data entry.',
    permissions: [
      Permissions.CREATE_JOURNAL_ENTRY,
      Permissions.VIEW_JOURNAL,
      Permissions.GENERATE_PL_REPORT,
      Permissions.GENERATE_BS_REPORT,
    ],
  }
};
