# Epic: Secure Access and Role Control

**Epic ID:** EPIC-01
**Related PRD:** specs/prds/PRD-innovatepam-portal.md
**Author:** GitHub Copilot
**Status:** Backlog
**Target Release:** MVP Wave 1
**Last Updated:** 2026-02-24

---

## 1. Description

This epic delivers secure authentication and role-based access for internal users of InnovatEPAM Portal. It enables employees to register and sign in safely, then receive Submitter or Admin capabilities based on authorization policies. This creates the trust and control foundation required for all idea submission and evaluation workflows.

---

## 2. Primary Persona

**Persona:** Elif, the Innovation Program Manager

**Why they benefit:** Elif needs strict role enforcement so only authorized admins can evaluate and change idea outcomes. Strong access control prevents unauthorized workflow changes and preserves program integrity.

---

## 3. Success Criteria

- [ ] Employees can register and log in via authenticated flows, and protected routes reject unauthenticated access.
- [ ] Role-based permissions enforce Submitter/Admin access boundaries across UI and API endpoints with zero high-severity authorization defects in UAT.
- [ ] Authenticated endpoint reliability reaches at least 99.0% successful requests per month (traceable to PRD metric: API reliability for authenticated endpoints).
- [ ] Authentication and authorization behavior is covered by automated tests included in MVP quality gates.

---

## 4. Scope / Complexity

**Estimate:** M

**Justification:** This epic spans identity flows, token lifecycle handling, and server-enforced authorization rules across frontend and backend surfaces.

### In Scope
- Employee registration and login with signed JWT issuance and expiry handling.
- Protected route and API middleware enforcement for authenticated access.
- Role-based access enforcement for Submitter and Admin actions.
- Auth-related acceptance and regression tests.

### Out of Scope
- Single sign-on federation beyond MVP authentication pattern.
- Guest or external-user access.
- Fine-grained custom permission editor.

---

## 5. Dependencies

| Dependency                          | Type                          | Status              | Owner / Notes                  |
|-------------------------------------|-------------------------------|---------------------|-------------------------------|
| Corporate identity/auth integration | External | Pending | Platform/Security team alignment required |
| JWT signing key management          | Technical | Pending | DevOps and backend setup required |
| Security validation checklist       | Design | Pending | Security team sign-off before release |

---

## 6. User Stories

> ⚠️ Stories have not been written yet. This section will be populated during sprint planning or backlog refinement.

| Story ID   | Title                          | Status              |
|------------|--------------------------------|---------------------|
| US-101   | As an EPAM employee, I want to register an account using corporate identity details | Backlog |
| US-102   | As an EPAM employee, I want to log in and receive a valid session token | Backlog |
| US-103   | As an admin, I want access blocked for non-admin users on moderation endpoints | Backlog |
| US-104   | As a submitter, I want unauthorized admin actions hidden and blocked so I only see permitted actions | Backlog |
| US-105   | As a security reviewer, I want automated tests for auth and role checks so regressions are caught early | Backlog |

---

## Notes & Open Questions

- [ ] Confirm whether corporate directory attributes provide role assignment directly or via internal mapping.
- [ ] Confirm token expiration and refresh policy for MVP.
