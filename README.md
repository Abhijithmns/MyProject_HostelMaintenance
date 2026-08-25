# Lab 1 – Requirements Engineering & UML Use-Case Modelling

**Course:** Software Engineering Lab (Dept. of CSE, PES University)  
**Problem Statement #07:** Hostel Maintenance & Issue Ticketing System  
**Primary Domain:** Campus & Academic Operations  
**Target Stakeholders / Actors:** Hostel Resident, Maintenance Warden, Maintenance Staff  

---

## Overview

Hostel administration requires a geo-tagged ticketing pipeline to report plumbing, electrical, and carpentry issues, dispatch maintenance staff, track SLA timelines, and record resident closure sign-offs.

---

## 1. Requirements Table

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-001** | Functional | The system shall enable residents to log maintenance tickets with room number tags, photo attachments, and categorized issue severity. | High | **Pass:** Ticket is created, assigned a unique ID, and routed to warden queue;<br>**Fail:** Incomplete form accepted without room tag. | Core ticketing functionality for reporting maintenance issues. |
| **FR-002** | Functional | The system shall allow the Maintenance Warden to review pending tickets and assign them to available maintenance staff members. | High | **Pass:** Ticket status updates to "Assigned" and notification is sent to staff;<br>**Fail:** Ticket remains unassigned. | Required for technician dispatch and workload distribution. |
| **FR-003** | Functional | The system shall track ticket SLA timelines and display real-time status updates (Logged, Assigned, In-Progress, Resolved, Closed). | High | **Pass:** Status timestamp updates within 2 seconds;<br>**Fail:** Status update fails or SLA timer is inaccurate. | Enables tracking and real-time monitoring of resolution speed. |
| **FR-004** | Functional | The system shall require maintenance staff to attach geo-tagged proof-of-work photos upon marking a ticket as resolved. | Medium | **Pass:** Work photo with valid GPS metadata saved to ticket;<br>**Fail:** Ticket marked resolved without photo attachment. | Verifies physical presence and completion of maintenance work. |
| **FR-005** | Functional | The system shall allow the Hostel Resident to review resolved tickets and record a final closure sign-off or reopen if unsatisfied. | High | **Pass:** Status changes to "Closed" upon resident sign-off;<br>**Fail:** Ticket auto-closes without resident confirmation. | Ensures resident satisfaction before ticket is permanently closed. |
| **NFR-001** | Non-Functional (Performance & Security) | The system shall trigger automated escalation SMS/Email alerts if high-priority tickets exceed a 24-hour SLA without status change. | High | **Pass:** Benchmarking tests confirm target latency and security standards under simulated peak load;<br>**Fail:** Alert delayed or missing. | Prevents SLA breach on urgent maintenance issues. |
| **NFR-002** | Non-Functional (Availability & Reliability) | The system shall maintain 99.5% uptime during academic terms and support concurrent logging of up to 500 maintenance tickets per hour without data loss. | High | **Pass:** Uptime logs confirm ≥99.5% availability and zero data corruption under load;<br>**Fail:** Downtime >0.5% or data dropped. | Guarantees continuous availability during peak student residence periods. |

---

## 2. UML Use-Case Diagram

The UML Use-Case diagram below models all primary actors (`Hostel Resident`, `Maintenance Warden`, `Maintenance Staff`), primary use cases (`UC-01` through `UC-05`), and relationships including `«include»` and `«extend»`.

![UML Use Case Diagram](UML_image.drawio.png)

### Draw.io XML Code
The diagram source code is saved in [`UML_diagram.drawio`](file:///home/abhijith/pes/sem5/se/lab1_activity1_abhijith_pes1ug24cs252/UML_diagram.drawio) and can be opened/imported directly into [Draw.io](https://app.diagrams.net).

---

## 3. Use-Case Flow Specification

### Use Case ID & Name: `UC-01: Log Maintenance Ticket`
* **Primary Actor:** Hostel Resident
* **Preconditions:**
  1. Resident is logged into the Hostel Maintenance Portal.
  2. Resident profile is linked to a valid room tag and hostel block.
* **Postconditions:**
  1. Ticket is created with a unique Ticket ID and status `Logged`.
  2. Ticket is routed to the Maintenance Warden queue for staff assignment.

#### Main Success Scenario
1. Resident selects "Log Maintenance Ticket" from the portal menu.
2. System displays ticket form prepopulated with resident room tag and block details.
3. Resident selects issue category (Plumbing / Electrical / Carpentry) and severity (Low / Medium / High).
4. Resident enters issue description, attaches photo, and confirms location geo-tag (`UC-07`).
5. Resident submits the form.
6. System validates room tag, severity, and photo attachment.
7. System generates a unique Ticket ID and sets status to `Logged`.
8. System routes ticket to Warden dispatch queue.
9. System displays confirmation alert with Ticket ID to Resident.
10. Use case ends successfully.

#### Alternate Flow: 4a. Incomplete Form Submission
1. At step 6, system detects missing room tag or photo attachment.
2. System displays error prompt: *"Room tag and photo attachment are mandatory."*
3. Resident provides missing information and resubmits.
4. Flow resumes at Step 6.
