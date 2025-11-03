## Coding Expectations
Each contributor shall commit $5000$ lines of code. 

The following technology stack shall be used:
- Ubuntu Server `24.04.3`,
- Python `3.14.0`,
- Django `5.2.7`,
- Gunicorn `23.0.0`,
- PostgreSQL `18.0`,
- Node.js `22.21.0`,
- Vue `3.5.22`,
- Tailwind `4.1`,
- DaisyUI `5.3.8`

```
		 Client
		 │
		 ▼
┌─────────────────┐
│ (reverse proxy) │
└────────┬────────┘
		 │ (:8080)
         ▼
┌─────────────────┐
│ Gunicorn        │
└────────┬────────┘
         │
         ▼
         Django
         │
         ▼
         PostgreSQL
```

Note: Pandas shall be used as the primary visualisation tool until replaced.

## Documentation Expectations
All functions shall be documented.

Function documentation shall include @brief, @param, and @return descriptions.

## Testing Expectations:
All branches shall pass a full-feature test prior to merge.

All pull request shall be reviewed by at least two contributors.

If any feature breaks post merge, every contributor shall inspect the failure and contribute to its resolution

Every commit shall be of the form: `<infinitive> <context> to <reason>`. e.g., Add feature to component to support non-functional requirement #123. If the reason statement is reasonably long, transition the statement to the description box.

## Timeline

### Nov. 15 - Prototype v0
From PA2: Implement a minimal-feature data visualisation tool. This is the first of our Semester 1 intermediary goals. This implementation shall meet the minimal data visualisation requirements provided to us by the Department of Physics and its completion shall signal the first round of feedback. The deadline for this implementation is November 15th.

### Nov. 21 - Prototype v1
From PA2: Implement a minimal-feature front-end querying system. This is the second of our Semester 1 intermediary goals. This implementation shall enable the extraction and visualisation of raw data from the back-end database and is to be implemented at the request of the Department of Physics. The deadline for this implementation is November 21st.

### Dec. 6 - Prototype v2
From PA2: Implement a minimal-feature account organisation system. This is the third and last of our Semester 1 intermediary goals. This implementation shall support a user-hierarchy through the creation, deletion, and modification of user accounts and is to be implemented at the request of Vinh Le. The deadline for this implementation is December 6th.