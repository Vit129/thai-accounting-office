# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool is connected in Claude
Desktop for that category. The skills describe the work by category, so the same plugin
works on Google Workspace or Microsoft 365.

## Connectors for this plugin

| Category       | Placeholder        | Options                                   |
| -------------- | ------------------ | ----------------------------------------- |
| Email          | `~~email`          | Gmail, Outlook                            |
| Spreadsheet    | `~~spreadsheet`    | Google Sheets, Excel files (.xlsx)        |
| Cloud storage  | `~~cloud storage`  | Google Drive, OneDrive / SharePoint       |
| Calendar       | `~~calendar`       | Google Calendar, Outlook Calendar         |

Connect the ones you use in Claude Desktop → Settings → Connectors. Excel and PDF files
also work without any connector when they are in the folder you share with Claude.
