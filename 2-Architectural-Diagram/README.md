# 2-Architectural-Diagram

**Problem Statement #07:** Hostel Maintenance & Issue Ticketing System  

---

## 1. Architectural Overview

The system is designed following a **4-Tier Layered and Component Architecture** with modular microservices, decoupled data persistence, and external service gateways.

### Diagram File
- Editable Draw.io XML file: [architecture_diagram.drawio](file:///home/abhijith/pes/sem5/lab1_activity1_abhijith_pes1ug24cs252/2-Architectural-Diagram/architecture_diagram.drawio)

---

## 2. Layer-by-Layer Architectural Breakdown

### Tier 1: Presentation & Client Interface Layer
- **Hostel Resident Client (Web & Mobile App)**:
  - Enables residents to log maintenance tickets with room number tags, categories (Plumbing, Electrical, Carpentry), and issue photos.
  - Allows residents to inspect resolved tickets and provide final closure sign-off or initiate a ticket reopen.
- **Maintenance Warden Portal (Web Management Console)**:
  - Provides a centralized queue triage dashboard for reviewing pending tickets.
  - Supports staff allocation based on trade skills and workload.
  - Monitors real-time SLA countdown timers and escalation statuses.
- **Maintenance Staff Field App (Mobile Work Order App)**:
  - Displays assigned work orders and repair instructions.
  - Enables field technicians to update status to "In-Progress".
  - Enforces capturing geo-tagged proof-of-work photos with hardware GPS metadata prior to marking tickets as "Resolved".

### Tier 2: API Gateway & Security Layer
- **API Gateway & Reverse Proxy**:
  - Serves as the single entry point for all client requests over HTTPS (TLS 1.3).
  - Handles rate limiting (enforcing the NFR-002 capacity of 500 requests/hour), request routing, and load balancing.
- **Authentication & RBAC Middleware**:
  - Verifies JSON Web Tokens (JWT) on each incoming request.
  - Enforces Role-Based Access Control (RBAC) across three roles: Resident, Maintenance Warden, and Maintenance Staff.

### Tier 3: Application & Business Logic Layer (Core Microservices)
- **Ticket Management Service (FR-001, FR-003)**:
  - Manages ticket lifecycle states: `Logged` -> `Assigned` -> `In-Progress` -> `Resolved` -> `Closed` (or `Reopened`).
  - Validates room number tags, photo attachments, and categorized issue severity.
- **Dispatch & Assignment Service (FR-002)**:
  - Facilitates warden review and technician allocation.
  - Dispatches assignment events and routes work orders to staff queues.
- **Geo-Tag & Media Verification Service (FR-004)**:
  - Extracts EXIF GPS metadata from uploaded resolution photos.
  - Validates coordinates against the registered hostel block boundary to prevent fraudulent sign-offs.
- **SLA Tracking & Escalation Engine (NFR-001, FR-003)**:
  - Tracks SLA countdown timers with sub-2-second timestamp precision.
  - Detects threshold breaches (e.g., high-priority issues pending > 24 hours without status change) and triggers automated escalations.
- **Closure & Sign-off Service (FR-005)**:
  - Manages resident verification workflows, capturing formal sign-off or triggering ticket reopening.
- **Notification & Messaging Service (NFR-001)**:
  - Manages in-app notifications and routes critical alerts to external SMS/Email channels.

### Tier 4: Data Persistence & Infrastructure Layer
- **Relational Database (PostgreSQL / MySQL)**:
  - Stores transactional data: user credentials, room allocations, ticket records, staff assignments, and audit trails.
- **Object Storage (AWS S3 / MinIO)**:
  - Stores encrypted resident issue photos and technician geo-tagged proof-of-work images.
- **In-Memory Cache & Message Broker (Redis / RabbitMQ)**:
  - Caches active user sessions and real-time ticket states.
  - Serves as the priority task queue for SLA countdown jobs and escalation event pub/sub.

### Tier 5: External Systems & Gateways
- **SMS & Email Escalation Gateway (Twilio / SendGrid / AWS SNS)**:
  - Dispatches automated SMS and email alerts when high-priority tickets breach the 24-hour SLA.
- **Hostel GIS & Geo-Fence Service**:
  - Validates latitude/longitude coordinates against the campus physical boundaries.

---

## 3. How to Open and Edit the Diagram
1. Visit [Draw.io / diagrams.net](https://app.diagrams.net).
2. Select **Open Existing Diagram** (or go to **File > Open From > Device**).
3. Select [`architecture_diagram.drawio`](file:///home/abhijith/pes/sem5/lab1_activity1_abhijith_pes1ug24cs252/2-Architectural-Diagram/architecture_diagram.drawio).
4. To export an image: go to **File > Export as > PNG** (set zoom to 200% or 300% for high resolution).
