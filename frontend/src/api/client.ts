export type ComplaintPayload = {
  text: string;
  location: string;
  reporter_contact?: string;
};

export type Complaint = {
  id: string;
  text: string;
  location: string;
  reporter_contact: string | null;
  category: string;
  priority: string;
  status: string;
  ai_summary: string;
  triaged_by: string;
  triage_latency_ms: number;
  created_at: string;
  updated_at: string;
};

export function getBaseUrl(): string {
  return "/api";
}

export async function postComplaint(payload: ComplaintPayload): Promise<Complaint> {
  const response = await fetch(`${getBaseUrl()}/complaints`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const body = (await response.json()) as { detail?: string };
      if (body.detail) message = body.detail;
    } catch {
      // Preserve the status message when the server response is not JSON.
    }
    throw new Error(message);
  }

  return (await response.json()) as Complaint;
}
