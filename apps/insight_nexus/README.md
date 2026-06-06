# Insight-Nexus

Multi-sector remote employee check-in and attendance system seamlessly integrated with ERPNext.

## Features

- Employee check-in/check-out tracking
- Optional GPS location tracking
- Real-time sync with ERPNext Attendance and Employee Checkin DocTypes
- Multi-tenant support (IHTS, ITMC, IICC, ITT)
- Secure authentication
- History and reporting

## Installation

```bash
cd /path/to/frappe-bench
bench get-app https://github.com/iicc/insight-nexus
bench --site 26i.uk install-app insight_nexus
```

## Configuration

Set the following in your site config:

```
"insight_nexus": {
    "gps_accuracy_threshold": 50,
    "check_in_cooldown_minutes": 15
}
```

## License

MIT
